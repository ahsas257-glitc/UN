"""Shared renderer for questionnaire-specific organization dashboards."""

from __future__ import annotations

import pandas as pd

from un_dashboard.design import ThemeMode
from un_dashboard.questionnaires.base import QuestionnaireSchema
from un_dashboard.views.adaptive_dashboard import render_adaptive_dashboard


def render_questionnaire_dashboard(
    org_data: pd.DataFrame,
    project_name: str,
    forms_dir: str,
    template: str,
    theme_mode: ThemeMode,
    questionnaire: QuestionnaireSchema,
) -> None:
    render_adaptive_dashboard(
        org_data=org_data,
        project_name=project_name,
        forms_dir=forms_dir,
        template=template,
        theme_mode=theme_mode,
        questionnaire=questionnaire,
    )
