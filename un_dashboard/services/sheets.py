"""Google Sheets data access layer."""

from __future__ import annotations

import io
import json
import re
import time
from typing import Any, Dict, Optional, Sequence
from urllib.parse import quote

import pandas as pd
import requests
import streamlit as st
from requests import exceptions as req_exc

try:
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2.service_account import Credentials
except Exception:  # pragma: no cover - optional dependency at runtime
    AuthorizedSession = None
    Credentials = None


RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
READONLY_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]
READWRITE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def parse_sheet_id(sheet_url: str) -> str:
    raw = str(sheet_url).strip()
    if re.fullmatch(r"[a-zA-Z0-9-_]{20,}", raw):
        return raw

    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", raw)
    if not match:
        raise ValueError("Invalid Google Sheet URL.")
    return match.group(1)


def _retry_delay(attempt: int) -> float:
    return min(6.0, 0.6 * (2 ** max(attempt - 1, 0)))


def _request_with_retries(
    session: requests.Session,
    method: str,
    url: str,
    *,
    tries: int = 4,
    timeout: int = 30,
    **kwargs: Any,
) -> requests.Response:
    last_err = None
    for attempt in range(1, tries + 1):
        try:
            resp = session.request(method, url, timeout=timeout, **kwargs)
            if resp.status_code in RETRYABLE_STATUS_CODES:
                raise req_exc.HTTPError(f"Retryable HTTP {resp.status_code}", response=resp)
            resp.raise_for_status()
            return resp
        except (req_exc.RequestException, OSError) as exc:  # Connection reset, TLS, timeouts, etc.
            last_err = exc
            if attempt < tries:
                time.sleep(_retry_delay(attempt))
                continue
            raise
    if last_err:
        raise last_err
    raise RuntimeError("Request failed without an exception.")


def _http_get_with_retries(url: str, *, tries: int = 4, timeout: int = 30) -> requests.Response:
    with requests.Session() as session:
        session.headers.update({"User-Agent": "UNDashboard/1.0"})
        return _request_with_retries(session, "GET", url, tries=tries, timeout=timeout)


def _dedupe_header(header: Sequence[str]) -> list[str]:
    """
    Make worksheet headers unique (pandas-like): col, col.1, col.2, ...
    This prevents ambiguous DataFrame selection when source sheets contain duplicate labels.
    """
    out: list[str] = []
    seen: dict[str, int] = {}
    for raw in header:
        base = str(raw or "").strip()
        if not base:
            base = "unnamed"
        if base not in seen:
            seen[base] = 0
            out.append(base)
            continue
        seen[base] += 1
        out.append(f"{base}.{seen[base]}")
    return out


def get_secret(name: str) -> str:
    try:
        value = st.secrets[name]
    except Exception:
        return ""
    return str(value) if value is not None else ""


def get_service_account_info() -> Optional[Dict[str, Any]]:
    try:
        if "gcp_service_account" in st.secrets:
            return dict(st.secrets["gcp_service_account"])
    except Exception:
        pass

    raw = get_secret("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _normalize_values(values: Sequence[Sequence[Any]]) -> pd.DataFrame:
    if not values:
        return pd.DataFrame()

    header = [str(x).strip() for x in values[0]]
    rows = [list(row) for row in values[1:]]
    width = max([len(header)] + [len(r) for r in rows] + [1])
    header = header + [f"unnamed_{i}" for i in range(len(header), width)]
    header = _dedupe_header(header)
    rows = [r + [""] * (width - len(r)) for r in rows]
    return pd.DataFrame(rows, columns=header)


def _quoted_sheet_title(title: str) -> str:
    escaped = str(title).replace("'", "''")
    return f"'{escaped}'"


def _encoded_range(sheet_range: str) -> str:
    return quote(sheet_range, safe="")


def _service_credentials(service_info: Dict[str, Any], scopes: Sequence[str]):
    if Credentials is None:
        raise RuntimeError("google-auth is not installed.")
    return Credentials.from_service_account_info(service_info, scopes=list(scopes))


def _authorized_http_session(service_info: Optional[Dict[str, Any]], *, read_only: bool) -> AuthorizedSession:
    if AuthorizedSession is None or Credentials is None:
        raise RuntimeError("google-auth is not installed.")
    if not service_info:
        raise RuntimeError("Google service account is required.")

    scopes = READONLY_SCOPES if read_only else READWRITE_SCOPES
    creds = _service_credentials(service_info, scopes)
    session = AuthorizedSession(creds)
    session.headers.update({"User-Agent": "UNDashboard/1.0"})
    return session


def _private_metadata(sheet_id: str, service_info: Dict[str, Any]) -> list[str]:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
    params = {"fields": "sheets(properties(title))"}
    with _authorized_http_session(service_info, read_only=True) as session:
        response = _request_with_retries(session, "GET", url, tries=4, timeout=30, params=params)
    payload = response.json()
    sheets = payload.get("sheets", [])
    return [sheet.get("properties", {}).get("title", "").strip() for sheet in sheets if sheet.get("properties", {}).get("title")]



def _private_values_batch(
    sheet_id: str,
    titles: Sequence[str],
    service_info: Dict[str, Any],
) -> Dict[str, pd.DataFrame]:
    if not titles:
        return {}

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values:batchGet"
    params: list[tuple[str, str]] = [("majorDimension", "ROWS")]
    params.extend(("ranges", _quoted_sheet_title(title)) for title in titles)

    with _authorized_http_session(service_info, read_only=True) as session:
        response = _request_with_retries(session, "GET", url, tries=4, timeout=60, params=params)

    payload = response.json()
    value_ranges = payload.get("valueRanges", [])
    out: Dict[str, pd.DataFrame] = {}
    for title, value_range in zip(titles, value_ranges):
        values = value_range.get("values", [])
        out[title] = _normalize_values(values)

    for title in titles:
        out.setdefault(title, pd.DataFrame())

    return out


def _private_values_get(
    sheet_id: str,
    sheet_range: str,
    service_info: Dict[str, Any],
) -> list[list[Any]]:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{_encoded_range(sheet_range)}"
    params = {"majorDimension": "ROWS"}
    with _authorized_http_session(service_info, read_only=True) as session:
        response = _request_with_retries(session, "GET", url, tries=4, timeout=30, params=params)
    payload = response.json()
    return payload.get("values", [])


def _private_values_update(
    sheet_id: str,
    sheet_range: str,
    values: list[list[Any]],
    service_info: Dict[str, Any],
) -> None:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{_encoded_range(sheet_range)}"
    params = {"valueInputOption": "RAW"}
    payload = {"majorDimension": "ROWS", "values": values}
    with _authorized_http_session(service_info, read_only=False) as session:
        _request_with_retries(session, "PUT", url, tries=4, timeout=30, params=params, json=payload)


def _private_values_append(
    sheet_id: str,
    sheet_range: str,
    values: list[list[Any]],
    service_info: Dict[str, Any],
) -> None:
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{_encoded_range(sheet_range)}:append"
    params = {"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"}
    payload = {"majorDimension": "ROWS", "values": values}
    with _authorized_http_session(service_info, read_only=False) as session:
        _request_with_retries(session, "POST", url, tries=4, timeout=30, params=params, json=payload)


@st.cache_data(show_spinner=False, ttl=300)
def load_workbook_public(sheet_id: str) -> Dict[str, pd.DataFrame]:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    response = _http_get_with_retries(url, tries=4, timeout=40)
    workbook = pd.read_excel(io.BytesIO(response.content), sheet_name=None)
    normalized: Dict[str, pd.DataFrame] = {}
    for title, frame in workbook.items():
        df = frame.copy()
        df.columns = _dedupe_header([str(col).strip() for col in df.columns])
        normalized[title] = df
    return normalized


@st.cache_data(show_spinner=False, ttl=300)
def load_workbook_private(sheet_id: str, service_info: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    titles = _private_metadata(sheet_id, service_info)
    return _private_values_batch(sheet_id, titles, service_info)



def load_workbook(sheet_url: str, service_info: Optional[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
    sheet_id = parse_sheet_id(sheet_url)
    prefer_private = bool(service_info)
    try:
        prefer_private = bool(st.secrets.get("FORCE_PRIVATE_FIRST", prefer_private))
    except Exception:
        pass

    loaders = []
    if prefer_private and service_info:
        loaders.append(("private", lambda: load_workbook_private(sheet_id, service_info)))
        loaders.append(("public", lambda: load_workbook_public(sheet_id)))
    else:
        loaders.append(("public", lambda: load_workbook_public(sheet_id)))
        if service_info:
            loaders.append(("private", lambda: load_workbook_private(sheet_id, service_info)))

    failures: list[tuple[str, Exception]] = []
    for name, loader in loaders:
        try:
            return loader()
        except Exception as exc:
            failures.append((name, exc))
            continue

    if failures:
        details = "; ".join(f"{name} load failed: {exc}" for name, exc in failures)
        raise RuntimeError(details) from failures[-1][1]
    raise RuntimeError("Could not load workbook.")


@st.cache_data(show_spinner=False, ttl=300)
def list_worksheet_titles(sheet_id: str, service_info: Optional[Dict[str, Any]]) -> list[str]:
    if not service_info:
        raise RuntimeError("Google service account is required.")
    return _private_metadata(sheet_id, service_info)


@st.cache_data(show_spinner=False, ttl=120)
def get_worksheet_header(
    sheet_id: str,
    worksheet_title: str,
    service_info: Optional[Dict[str, Any]],
) -> list[str]:
    if not service_info:
        raise RuntimeError("Google service account is required.")
    values = _private_values_get(sheet_id, f"{_quoted_sheet_title(worksheet_title)}!1:1", service_info)
    if not values:
        return []
    return [str(x).strip() for x in values[0]]



def update_worksheet_header(
    sheet_id: str,
    worksheet_title: str,
    header: Sequence[str],
    service_info: Optional[Dict[str, Any]],
) -> None:
    if not service_info:
        raise RuntimeError("Google service account is required.")
    row = [str(x).strip() for x in header]
    _private_values_update(sheet_id, f"{_quoted_sheet_title(worksheet_title)}!A1", [row], service_info)



def append_worksheet_rows(
    sheet_id: str,
    worksheet_title: str,
    rows: list[list[object]],
    service_info: Optional[Dict[str, Any]],
) -> None:
    if not rows:
        return
    if not service_info:
        raise RuntimeError("Google service account is required.")
    _private_values_append(sheet_id, _quoted_sheet_title(worksheet_title), rows, service_info)


@st.cache_data(show_spinner=False, ttl=120)
def load_worksheet_df(
    sheet_id: str,
    worksheet_title: str,
    service_info: Optional[Dict[str, Any]],
) -> pd.DataFrame:
    if not service_info:
        raise RuntimeError("Google service account is required.")
    values = _private_values_get(sheet_id, _quoted_sheet_title(worksheet_title), service_info)
    return _normalize_values(values)
