"""Export utilities for downloadable reports."""

from __future__ import annotations

import io
from typing import Dict

import pandas as pd


def to_excel_bytes(sheets: Dict[str, pd.DataFrame]) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, index=False, sheet_name=(str(name)[:31] or "Sheet"))
    return buffer.getvalue()
