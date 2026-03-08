"""Router for organization dashboards by questionnaire key."""

from __future__ import annotations

import pandas as pd

from un_dashboard.design import ThemeMode
from un_dashboard.questionnaires.base import QuestionnaireSchema
from un_dashboard.views.adsdo_dashboard import render_adsdo_dashboard
from un_dashboard.views.anbo_dashboard import render_anbo_dashboard
from un_dashboard.views.arwe_dashboard import render_arwe_dashboard
from un_dashboard.views.aspso_dashboard import render_aspso_dashboard
from un_dashboard.views.dhdo_men_dashboard import render_dhdo_men_dashboard
from un_dashboard.views.dhdo_women_dashboard import render_dhdo_women_dashboard
from un_dashboard.views.ecoc_dashboard import render_ecoc_dashboard
from un_dashboard.views.ecoc_guardians_dashboard import render_ecoc_guardians_dashboard
from un_dashboard.views.gsro_dashboard import render_gsro_dashboard
from un_dashboard.views.hhso_dashboard import render_hhso_dashboard
from un_dashboard.views.hosaa_dashboard import render_hosaa_dashboard
from un_dashboard.views.ohad_dashboard import render_ohad_dashboard
from un_dashboard.views.orstw_dashboard import render_orstw_dashboard
from un_dashboard.views.ptcro_dashboard import render_ptcro_dashboard
from un_dashboard.views.rpo_dashboard import render_rpo_dashboard
from un_dashboard.views.unw_dashboard import render_unw_dashboard

DASHBOARD_RENDERERS = {
    "adsdo_beneficiaries": render_adsdo_dashboard,
    "anbo_beneficiaries": render_anbo_dashboard,
    "arwe_beneficiaries": render_arwe_dashboard,
    "aspso_beneficiaries": render_aspso_dashboard,
    "dhdo_beneficiaries_men": render_dhdo_men_dashboard,
    "dhdo_beneficiaries_women": render_dhdo_women_dashboard,
    "ecoc_beneficiaries": render_ecoc_dashboard,
    "ecoc_beneficiaries_male_guardians": render_ecoc_guardians_dashboard,
    "gsro_beneficiaries": render_gsro_dashboard,
    "hhso_beneficiaries": render_hhso_dashboard,
    "hosaa_beneficiaries": render_hosaa_dashboard,
    "ohad_beneficiaries": render_ohad_dashboard,
    "orstw_beneficiaries": render_orstw_dashboard,
    "ptcro_beneficiaries": render_ptcro_dashboard,
    "rpo_beneficiaries": render_rpo_dashboard,
    "unw_beneficiary": render_unw_dashboard,
}


def render_dashboard_by_questionnaire(
    org_data: pd.DataFrame,
    questionnaire: QuestionnaireSchema | None,
    project_name: str,
    forms_dir: str,
    template: str,
    theme_mode: ThemeMode,
) -> bool:
    if questionnaire is None:
        return False

    renderer = DASHBOARD_RENDERERS.get(questionnaire.key)
    if renderer is None:
        return False

    renderer(
        org_data=org_data,
        project_name=project_name,
        forms_dir=forms_dir,
        template=template,
        theme_mode=theme_mode,
    )
    return True
