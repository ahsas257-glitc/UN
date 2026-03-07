"""Questionnaire model definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence


@dataclass(frozen=True)
class QuestionnaireSchema:
    key: str
    title: str
    indicator_candidates: Mapping[str, Sequence[str]]
    org_dashboard_tabs: Mapping[str, Mapping[str, Sequence[str]]] = field(default_factory=dict)
    org_dashboard_tab_labels: Mapping[str, str] = field(default_factory=dict)
