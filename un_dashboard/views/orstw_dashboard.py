"""ORSTW organization dashboard renderer."""

from __future__ import annotations

import pandas as pd

from un_dashboard.design import ThemeMode
from un_dashboard.questionnaires.orstw_beneficiaries import SCHEMA
from un_dashboard.views.questionnaire_dashboard import render_questionnaire_dashboard


def render_orstw_dashboard(
    org_data: pd.DataFrame,
    project_name: str,
    forms_dir: str,
    template: str,
    theme_mode: ThemeMode,
) -> None:
    render_questionnaire_dashboard(
        org_data=org_data,
        project_name=project_name,
        forms_dir=forms_dir,
        template=template,
        theme_mode=theme_mode,
        questionnaire=SCHEMA,
    )
