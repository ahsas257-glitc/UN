"""Build questionnaire profiles (tabs + questions) from XLSForm survey sheets."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

_WRAPPER_GROUP_KEYS = {
    "questions",
    "quesitons",
    "question",
    "form",
    "end form",
    "end_form",
    "consent_ok",
}

_SKIP_TYPES_EXACT = {
    "",
    "begin_group",
    "end_group",
    "begin_repeat",
    "end_repeat",
    "calculate",
    "note",
    "start",
    "end",
    "today",
    "username",
    "deviceid",
    "subscriberid",
    "simserial",
    "phonenumber",
    "audit",
}


def _norm(value: str) -> str:
    return " ".join(str(value or "").strip().lower().replace("_", " ").split())


def _pick_col(df: pd.DataFrame, preferred: list[str]) -> str | None:
    if df.empty:
        return None
    lookup = {str(c).strip().lower(): c for c in df.columns}
    for key in preferred:
        if key in lookup:
            return lookup[key]
    for col in df.columns:
        lowered = str(col).strip().lower()
        for key in preferred:
            if key in lowered:
                return col
    return None


def _humanize(text: str) -> str:
    clean = re.sub(r"[_\-]+", " ", str(text or "")).strip()
    return clean.title() if clean else "General"


def _is_question_type(raw_type: str) -> bool:
    qtype = _norm(raw_type)
    if not qtype:
        return False
    if qtype in _SKIP_TYPES_EXACT:
        return False
    if qtype.startswith("begin ") or qtype.startswith("end "):
        return False
    if qtype.startswith("begin_") or qtype.startswith("end_"):
        return False
    if qtype.startswith("calculate") or qtype.startswith("note"):
        return False
    return True


def _is_begin_group(raw_type: str) -> bool:
    qtype = _norm(raw_type)
    return qtype.startswith("begin group") or qtype.startswith("begin_group") or qtype.startswith("begin repeat") or qtype.startswith("begin_repeat")


def _is_end_group(raw_type: str) -> bool:
    qtype = _norm(raw_type)
    return qtype.startswith("end group") or qtype.startswith("end_group") or qtype.startswith("end repeat") or qtype.startswith("end_repeat")


def _is_wrapper_group(group_name: str, group_label: str) -> bool:
    key = _norm(group_label or group_name)
    return key in _WRAPPER_GROUP_KEYS


def _dedupe_questions(questions: list[dict]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for q in questions:
        name = str(q.get("name", "")).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(q)
    return out


def _build_tabs_from_questions(sheet_name: str, questions: list[dict]) -> list[dict]:
    if not questions:
        return [{"key": "general", "label": "General", "questions": []}]

    tabs_map: dict[str, dict] = {}
    tab_order: list[str] = []

    for q in questions:
        path = q.get("group_path", []) or []
        chosen_group: dict | None = None

        meaningful = [g for g in path if not _is_wrapper_group(str(g.get("name", "")), str(g.get("label", "")))]
        if meaningful:
            # Top meaningful group keeps tabs close to XLSForm top-level sections.
            chosen_group = meaningful[0]
        elif path:
            chosen_group = path[0]

        if chosen_group:
            key = str(chosen_group.get("name") or "general").strip() or "general"
            label = str(chosen_group.get("label") or "").strip() or _humanize(key)
        else:
            key = "general"
            label = "General"

        tab_id = f"tab::{key}"
        if tab_id not in tabs_map:
            tabs_map[tab_id] = {"key": key, "label": label, "questions": []}
            tab_order.append(tab_id)
        tabs_map[tab_id]["questions"].append(q)

    tabs = [tabs_map[t] for t in tab_order]

    # Keep tab labels unique to avoid Streamlit tab collisions.
    seen_labels: dict[str, int] = {}
    for tab in tabs:
        label = str(tab["label"]).strip() or "General"
        count = seen_labels.get(label, 0)
        if count > 0:
            tab["label"] = f"{label} ({count + 1})"
        seen_labels[label] = count + 1

    return tabs


def _profile_from_questions(sheet_name: str, questions: list[dict], source: str) -> dict:
    deduped = _dedupe_questions(questions)
    tabs = _build_tabs_from_questions(sheet_name, deduped)
    return {
        "sheet_name": sheet_name,
        "source": source,
        "questions": deduped,
        "tabs": tabs,
    }


def _build_profile_from_xlsform(path: Path) -> dict:
    survey_df = pd.read_excel(path, sheet_name="survey")
    if survey_df is None or survey_df.empty:
        return _profile_from_questions(path.stem, [], source="xlsform")

    survey_df = survey_df.fillna("")
    type_col = _pick_col(survey_df, ["type"]) or "type"
    name_col = _pick_col(survey_df, ["name"]) or "name"
    label_col = _pick_col(survey_df, ["label::english", "label::english (en)", "label"])

    group_stack: list[dict] = []
    questions: list[dict] = []

    for _, row in survey_df.iterrows():
        qtype = str(row.get(type_col, "")).strip()
        name = str(row.get(name_col, "")).strip()
        label = str(row.get(label_col, "")).strip() if label_col else ""

        if _is_begin_group(qtype):
            g_name = name or f"group_{len(group_stack)+1}"
            g_label = label or _humanize(g_name)
            group_stack.append({"name": g_name, "label": g_label})
            continue

        if _is_end_group(qtype):
            if group_stack:
                group_stack.pop()
            continue

        if not name or not _is_question_type(qtype):
            continue

        if not label:
            label = _humanize(name)

        questions.append(
            {
                "name": name,
                "label": label,
                "type": qtype,
                "is_multi": _norm(qtype).startswith("select multiple"),
                "group_path": [dict(x) for x in group_stack],
            }
        )

    return _profile_from_questions(path.stem, questions, source="xlsform")


@st.cache_data(show_spinner=False, ttl=1800)
def load_form_profiles(forms_dir: str) -> dict[str, dict]:
    if not forms_dir:
        return {}

    base = Path(forms_dir)
    if not base.exists() or not base.is_dir():
        return {}

    out: dict[str, dict] = {}
    for path in sorted(base.glob("*.xlsx"), key=lambda p: p.name.lower()):
        try:
            out[path.stem] = _build_profile_from_xlsform(path)
        except Exception:
            continue
    return out


def build_fallback_profile(sheet_name: str, columns: Iterable[str]) -> dict:
    questions: list[dict] = []
    for raw in columns:
        name = str(raw or "").strip()
        if not name or name.lower().startswith("unnamed"):
            continue
        questions.append(
            {
                "name": name,
                "label": _humanize(name),
                "type": "unknown",
                "is_multi": False,
                "group_path": [],
            }
        )
    return _profile_from_questions(sheet_name, questions, source="fallback")


def resolve_profile(sheet_name: str, columns: Iterable[str], forms_dir: str) -> dict:
    profiles = load_form_profiles(forms_dir)
    if sheet_name in profiles:
        return profiles[sheet_name]
    return build_fallback_profile(sheet_name, columns)

