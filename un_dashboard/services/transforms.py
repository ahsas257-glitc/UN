"""Data transformation, normalization, and analytics helpers."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import streamlit as st

from un_dashboard.core.constants import (
    ARABIC_SCRIPT_RE,
    CORRECTION_LOG_SHEET,
    ORG_ALIASES,
    POSITIVE_VALUES,
    PROTECTED_COLUMNS,
    TARGET_INTERVIEWS_PER_ORG,
    YES_VALUES,
    org_master_frame,
)


def normalize_org_code(raw_code: str) -> str:
    code = re.sub(r"[^A-Za-z0-9]", "", str(raw_code or "").upper())
    return ORG_ALIASES.get(code, code)


def infer_org_code_from_sheet(sheet_name: str) -> str:
    return normalize_org_code(str(sheet_name).split("-")[0])


def find_column(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    if df.empty:
        return None

    lower_map = {str(c).lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]

    for candidate in candidates:
        token = candidate.lower()
        for col in df.columns:
            if token in str(col).lower():
                return col

    return None


def _column_as_series(df: pd.DataFrame, column: str) -> Optional[pd.Series]:
    """
    Return one Series for a column label.
    If duplicate labels exist, the first matching column is used.
    """
    if df.empty or not column or column not in df.columns:
        return None
    selected = df[column]
    if isinstance(selected, pd.DataFrame):
        if selected.shape[1] == 0:
            return None
        return selected.iloc[:, 0]
    return selected


def ensure_unique_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    out = df.copy()
    seen: dict[str, int] = {}
    columns: list[str] = []
    for raw in out.columns:
        base = str(raw).strip() or "unnamed"
        count = seen.get(base, 0)
        columns.append(base if count == 0 else f"{base}.{count}")
        seen[base] = count + 1
    out.columns = columns
    return out


def contains_non_english_text(value: Any) -> bool:
    if pd.isna(value):
        return False
    text = str(value).strip()
    return bool(text and ARABIC_SCRIPT_RE.search(text))


def hide_non_english(value: Any) -> Any:
    return "[Translation pending]" if contains_non_english_text(value) else value


def sanitize_for_display(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Use positional access so duplicate labels never break display sanitation.
    for idx in range(out.shape[1]):
        series = out.iloc[:, idx]
        if series.dtype == "object":
            out.iloc[:, idx] = series.map(hide_non_english)
    return out


def normalize_token(value: Any) -> str:
    text = str(value or "").strip().lower()
    return re.sub(r"[^\w\u0600-\u06FF]+", "", text)


def score_positive_rate(series: pd.Series | pd.DataFrame, positive: Optional[set[str]] = None) -> float:
    if isinstance(series, pd.DataFrame):
        if series.empty or series.shape[1] == 0:
            return float("nan")
        series = series.iloc[:, 0]

    normalized = series.dropna().astype(str).map(normalize_token)
    if normalized.empty:
        return float("nan")
    return float(normalized.isin(positive or POSITIVE_VALUES).mean())


def format_percent(value: float) -> str:
    return "—" if pd.isna(value) else f"{value * 100:.1f}%"


@st.cache_data(show_spinner=False, ttl=600)
def prepare_data_bundle(workbook: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    frames: List[pd.DataFrame] = []
    correction_log = pd.DataFrame(columns=["_uuid", "Label", "old_value", "new_value"])
    designed_orgs: List[str] = []

    for sheet_name, source_df in workbook.items():
        title = str(sheet_name).strip()
        if title.lower() == CORRECTION_LOG_SHEET.lower():
            correction_log = source_df.copy()
            continue

        org_code = infer_org_code_from_sheet(title)
        if org_code:
            designed_orgs.append(org_code)

        df = ensure_unique_columns(source_df.copy())
        if "_uuid" not in df.columns:
            alt_uuid = find_column(df, ["_uuid", "uuid", "instanceid", "_id"])
            alt_uuid_series = _column_as_series(df, alt_uuid) if alt_uuid else None
            df["_uuid"] = alt_uuid_series if alt_uuid_series is not None else [f"{title}-{i + 1}" for i in range(len(df))]

        df["org_code"] = org_code
        df["sheet_name"] = title
        frames.append(df)

    non_empty_frames = [frame for frame in frames if not frame.empty]
    combined = pd.concat(non_empty_frames, ignore_index=True, sort=False) if non_empty_frames else pd.DataFrame()
    return combined, correction_log, sorted(set([x for x in designed_orgs if x]))


@st.cache_data(show_spinner=False, ttl=600)
def clean_correction_log(df: pd.DataFrame) -> pd.DataFrame:
    required = ["_uuid", "Label", "old_value", "new_value"]
    if df is None or df.empty:
        return pd.DataFrame(columns=required)

    out = df.copy()
    for col in required:
        if col not in out.columns:
            out[col] = ""

    out = out[required].dropna(subset=["_uuid", "Label", "new_value"])
    for col in required:
        out[col] = out[col].astype(str).str.strip()

    out = out[(out["_uuid"] != "") & (out["Label"] != "")]
    return out.drop_duplicates(subset=["_uuid", "Label", "old_value"], keep="last")


@st.cache_data(show_spinner=False, ttl=600)
def apply_corrections(data: pd.DataFrame, correction_log: pd.DataFrame) -> pd.DataFrame:
    if data.empty or correction_log.empty or "_uuid" not in data.columns:
        return data.copy()

    corrected = data.copy()
    uuid_series = corrected["_uuid"].astype(str)

    for row in correction_log.to_dict("records"):
        uid = str(row["_uuid"]).strip()
        label = str(row["Label"]).strip()
        old_value = str(row["old_value"]).strip()
        new_value = str(row["new_value"]).strip()

        if label not in corrected.columns:
            continue

        base_mask = uuid_series.eq(uid)
        if not base_mask.any():
            continue

        if old_value:
            mask = base_mask & corrected[label].astype(str).eq(old_value)
        else:
            mask = base_mask

        if not mask.any():
            mask = base_mask

        corrected.loc[mask, label] = new_value

    return corrected


@st.cache_data(show_spinner=False, ttl=600)
def build_master_table(data_org_codes: Sequence[str], designed_orgs: Sequence[str]) -> pd.DataFrame:
    master = org_master_frame()
    known = set(master["org_code"].tolist())
    extra = sorted(set(data_org_codes).difference(known))
    if extra:
        ext_df = pd.DataFrame(
            [{"org_code": x, "province": "Unknown", "ingo_partner": "Unknown"} for x in extra]
        )
        master = pd.concat([master, ext_df], ignore_index=True)

    master["is_designed"] = master["org_code"].isin(set(designed_orgs))
    return master


@st.cache_data(show_spinner=False, ttl=600)
def build_progress_table(master: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    counts = data.groupby("org_code", dropna=False).size().rename("interviews").reset_index()
    out = master.merge(counts, on="org_code", how="left")
    out["interviews"] = out["interviews"].fillna(0).astype(int)
    out["target"] = TARGET_INTERVIEWS_PER_ORG
    out["progress_pct"] = np.where(out["target"] > 0, out["interviews"] / out["target"], np.nan)
    out["status"] = np.select(
        [
            out["interviews"] >= TARGET_INTERVIEWS_PER_ORG,
            out["interviews"] >= TARGET_INTERVIEWS_PER_ORG * 0.5,
            out["interviews"] > 0,
        ],
        ["Complete", "On Track", "Started"],
        default="No Data",
    )
    return out.sort_values(["progress_pct", "interviews"], ascending=[False, False])


def get_indicator_columns(
    df: pd.DataFrame,
    indicator_candidates: Mapping[str, Sequence[str]],
) -> Dict[str, Optional[str]]:
    return {key: find_column(df, candidates) for key, candidates in indicator_candidates.items()}


def existing_correction_keys(correction_log: pd.DataFrame) -> set[tuple[str, str, str]]:
    if correction_log.empty:
        return set()
    tmp = correction_log[["_uuid", "Label", "old_value"]].astype(str)
    return set(map(tuple, tmp.values.tolist()))


def collect_translation_candidates(
    data: pd.DataFrame,
    existing_keys: set[tuple[str, str, str]],
    max_cells: int,
) -> List[Dict[str, str]]:
    if data.empty or "_uuid" not in data.columns:
        return []

    candidates: List[Dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    for _, row in data.iterrows():
        uid = str(row.get("_uuid", "")).strip()
        if not uid:
            continue

        for col in data.columns:
            if col in PROTECTED_COLUMNS:
                continue

            value = row.get(col)
            if pd.isna(value):
                continue

            old_value = str(value).strip()
            if not old_value or not contains_non_english_text(old_value):
                continue

            key = (uid, col, old_value)
            if key in existing_keys or key in seen:
                continue

            seen.add(key)
            candidates.append({"_uuid": uid, "Label": col, "old_value": old_value})
            if len(candidates) >= max_cells:
                return candidates

    return candidates


def apply_filters(
    data: pd.DataFrame,
    selected_orgs: Sequence[str],
    selected_projects: Sequence[str],
    selected_partners: Sequence[str],
    selected_provinces: Sequence[str],
    consent_only: bool,
    consent_column: Optional[str],
) -> pd.DataFrame:
    filtered = data.copy()

    if selected_projects and "sheet_name" in filtered.columns:
        filtered = filtered[filtered["sheet_name"].astype(str).isin(selected_projects)]
    if selected_orgs:
        filtered = filtered[filtered["org_code"].isin(selected_orgs)]
    if selected_partners:
        filtered = filtered[filtered["ingo_partner"].isin(selected_partners)]
    if selected_provinces:
        filtered = filtered[filtered["province"].isin(selected_provinces)]

    if consent_only and consent_column and consent_column in filtered.columns:
        consent_series = _column_as_series(filtered, consent_column)
        if consent_series is not None:
            filtered = filtered[consent_series.map(normalize_token).isin(YES_VALUES)]

    return filtered


@st.cache_data(show_spinner=False, ttl=600)
def build_daily_interviews(data: pd.DataFrame, date_column: Optional[str]) -> pd.DataFrame:
    if data.empty or not date_column or date_column not in data.columns:
        return pd.DataFrame(columns=["date", "interviews", "cumulative"])

    date_series = _column_as_series(data, date_column)
    if date_series is None:
        return pd.DataFrame(columns=["date", "interviews", "cumulative"])

    # Force UTC parsing to avoid mixed-timezone object dtype that breaks `.dt`.
    parsed_dates = pd.to_datetime(date_series, errors="coerce", utc=True)

    if isinstance(parsed_dates, pd.DatetimeIndex):
        parsed_series = pd.Series(parsed_dates, index=data.index)
    elif isinstance(parsed_dates, pd.Series):
        parsed_series = parsed_dates
    else:
        parsed_series = pd.to_datetime(pd.Series(parsed_dates, index=data.index), errors="coerce", utc=True)

    temp = pd.DataFrame(index=data.index)
    temp["date"] = parsed_series.dt.tz_convert(None).dt.date
    temp = temp.dropna(subset=["date"])

    if temp.empty:
        return pd.DataFrame(columns=["date", "interviews", "cumulative"])

    daily = temp.groupby("date").size().rename("interviews").reset_index()
    daily = daily.sort_values("date")
    daily["cumulative"] = daily["interviews"].cumsum()
    return daily


@st.cache_data(show_spinner=False, ttl=600)
def build_org_daily_activity(
    data: pd.DataFrame,
    date_column: Optional[str],
    org_column: str = "org_code",
) -> pd.DataFrame:
    columns = ["org_code", "date", "weekday_num", "weekday_name", "interviews", "cumulative"]
    if data.empty or not date_column or date_column not in data.columns:
        return pd.DataFrame(columns=columns)

    date_series = _column_as_series(data, date_column)
    if date_series is None:
        return pd.DataFrame(columns=columns)

    parsed_dates = pd.to_datetime(date_series, errors="coerce", utc=True)
    if isinstance(parsed_dates, pd.DatetimeIndex):
        parsed_series = pd.Series(parsed_dates, index=data.index)
    elif isinstance(parsed_dates, pd.Series):
        parsed_series = parsed_dates
    else:
        parsed_series = pd.to_datetime(pd.Series(parsed_dates, index=data.index), errors="coerce", utc=True)

    temp = pd.DataFrame(index=data.index)
    temp["parsed_date"] = parsed_series.dt.tz_convert(None)
    temp = temp.dropna(subset=["parsed_date"])
    if temp.empty:
        return pd.DataFrame(columns=columns)

    if org_column in data.columns:
        temp["org_code"] = _column_as_series(data, org_column).astype(str)
    else:
        temp["org_code"] = "Current Scope"

    temp["date"] = temp["parsed_date"].dt.date
    temp["weekday_num"] = temp["parsed_date"].dt.dayofweek
    temp["weekday_name"] = temp["parsed_date"].dt.day_name()

    grouped = (
        temp.groupby(["org_code", "date", "weekday_num", "weekday_name"], dropna=False)
        .size()
        .rename("interviews")
        .reset_index()
        .sort_values(["org_code", "date"])
    )
    grouped["cumulative"] = grouped.groupby("org_code")["interviews"].cumsum()
    return grouped.reset_index(drop=True)


@st.cache_data(show_spinner=False, ttl=600)
def build_partner_province_matrix(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty or "ingo_partner" not in data.columns or "province" not in data.columns:
        return pd.DataFrame()

    temp = data.copy()
    temp["ingo_partner"] = temp["ingo_partner"].fillna("Unknown").astype(str)
    temp["province"] = temp["province"].fillna("Unknown").astype(str)
    matrix = pd.crosstab(temp["ingo_partner"], temp["province"])
    return matrix.reset_index()


@st.cache_data(show_spinner=False, ttl=600)
def top_orgs_by_progress(progress: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    if progress.empty:
        return progress
    cols = ["org_code", "province", "ingo_partner", "interviews", "target", "progress_pct", "status"]
    return progress.sort_values(["progress_pct", "interviews"], ascending=[False, False]).head(limit)[cols]
