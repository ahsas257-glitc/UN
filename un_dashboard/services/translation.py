"""Translation pipeline and correction_log writer."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

import streamlit as st
from openai import OpenAI

from un_dashboard.core.constants import CORRECTION_LOG_SHEET
from un_dashboard.services.transforms import contains_non_english_text

try:
    import gspread
    from google.oauth2.service_account import Credentials
    from gspread.exceptions import WorksheetNotFound
except Exception:  # pragma: no cover - optional dependency at runtime
    gspread = None
    Credentials = None
    WorksheetNotFound = Exception


def translate_one_answer(client: OpenAI, model: str, label: str, answer: str) -> str:
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert survey translator. Translate the answer to clear English using the "
                    "question label for context. Return only the translated answer text."
                ),
            },
            {"role": "user", "content": f"Question label: {label}\nAnswer: {answer}"},
        ],
    )
    translated = (response.choices[0].message.content or "").strip()
    translated = re.sub(r"\s+", " ", translated)
    return translated if translated and not contains_non_english_text(translated) else "Needs manual translation"


def translate_candidates(candidates: List[Dict[str, str]], api_key: str, model: str) -> List[Dict[str, str]]:
    if not candidates:
        return []

    client = OpenAI(api_key=api_key)
    pair_map: Dict[Tuple[str, str], str] = {}
    unique_pairs: List[Tuple[str, str]] = []

    for row in candidates:
        pair = (row["Label"], row["old_value"])
        if pair not in pair_map:
            pair_map[pair] = ""
            unique_pairs.append(pair)

    bar = st.progress(0.0)
    status = st.empty()
    total = len(unique_pairs)

    for i, (label, old_value) in enumerate(unique_pairs, start=1):
        status.caption(f"Translating {i}/{total}")
        try:
            pair_map[(label, old_value)] = translate_one_answer(client, model, label, old_value)
        except Exception:
            pair_map[(label, old_value)] = "Needs manual translation"
        bar.progress(i / total)

    bar.empty()
    status.empty()

    return [
        {
            "_uuid": row["_uuid"],
            "Label": row["Label"],
            "old_value": row["old_value"],
            "new_value": pair_map[(row["Label"], row["old_value"])],
        }
        for row in candidates
    ]


def append_to_correction_log(sheet_id: str, rows: List[Dict[str, str]], service_info: Dict[str, Any]) -> None:
    if not rows:
        return

    if gspread is None or Credentials is None:
        raise RuntimeError("gspread/google-auth are required.")

    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(service_info, scopes=scopes)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)

    try:
        worksheet = spreadsheet.worksheet(CORRECTION_LOG_SHEET)
    except WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=CORRECTION_LOG_SHEET, rows=1000, cols=8)
        worksheet.update("A1:D1", [["_uuid", "Label", "old_value", "new_value"]])

    if worksheet.row_values(1)[:4] != ["_uuid", "Label", "old_value", "new_value"]:
        worksheet.update("A1:D1", [["_uuid", "Label", "old_value", "new_value"]])

    payload = [[row["_uuid"], row["Label"], row["old_value"], row["new_value"]] for row in rows]
    worksheet.append_rows(payload, value_input_option="RAW")
