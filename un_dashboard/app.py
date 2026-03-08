"""Main Streamlit application entry for the UN Women dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from un_dashboard.core.constants import DEFAULT_INDICATOR_CANDIDATES, DEFAULT_SHEET_URL, DEFAULT_XLS_FORMS_DIR
from un_dashboard.design import (
    clickable_tabs,
    configure_page,
    inject_liquid_glass_theme,
    plotly_template_for,
    render_hero,
    resolve_theme_mode,
)
from un_dashboard.services.sheets import get_secret, get_service_account_info, load_workbook
from un_dashboard.services.transforms import (
    apply_corrections,
    apply_filters,
    build_master_table,
    build_progress_table,
    clean_correction_log,
    ensure_unique_columns,
    get_indicator_columns,
    prepare_data_bundle,
)
from un_dashboard.views.organization import render_organization_section
from un_dashboard.views.public import render_advanced_insights, render_public_dashboard, render_public_report


def _sorted_non_empty_options(df: pd.DataFrame, column: str) -> list[str]:
    if column not in df.columns:
        return []
    return sorted([x for x in df[column].dropna().astype(str).unique().tolist() if x])


def _ordered_project_options(df: pd.DataFrame) -> list[str]:
    from un_dashboard.core.constants import ORG_SHEET_TABS

    if "sheet_name" not in df.columns:
        return ORG_SHEET_TABS.copy()

    available = {x for x in _sorted_non_empty_options(df, "sheet_name")}
    extras = sorted([name for name in available if name not in set(ORG_SHEET_TABS)], key=str.lower)
    return ORG_SHEET_TABS.copy() + extras


def main() -> None:
    configure_page()

    service_info = get_service_account_info()
    gsheet_id = get_secret("GSHEET_ID")
    sheet_url = (
        get_secret("SHEET_URL")
        or get_secret("GOOGLE_SHEET_URL")
        or (
            f"https://docs.google.com/spreadsheets/d/{gsheet_id}/edit"
            if gsheet_id
            else DEFAULT_SHEET_URL
        )
    )
    forms_dir = get_secret("XLS_FORMS_DIR") or DEFAULT_XLS_FORMS_DIR
    openai_key = get_secret("OPENAI_API_KEY")
    openai_model = get_secret("OPENAI_MODEL") or "gpt-4o-mini"

    theme_mode = resolve_theme_mode()
    inject_liquid_glass_theme(theme_mode)
    template = plotly_template_for(theme_mode)

    render_hero()


    try:
        with st.spinner("Loading workbook..."):
            workbook = load_workbook(sheet_url, service_info)
    except Exception as exc:
        st.error(f"Unable to load Google Sheet: {exc}")
        st.stop()

    raw_data, correction_log_raw, designed_orgs = prepare_data_bundle(workbook)
    correction_log = clean_correction_log(correction_log_raw)
    corrected_data = apply_corrections(raw_data, correction_log)

    all_org_codes = corrected_data["org_code"].dropna().astype(str).tolist() if not corrected_data.empty else []
    master = build_master_table(all_org_codes, designed_orgs)

    if corrected_data.empty:
        data = corrected_data.copy()
        for col in ["org_code", "province", "ingo_partner"]:
            if col not in data.columns:
                data[col] = pd.Series(dtype="object")
    else:
        data = corrected_data.merge(master[["org_code", "province", "ingo_partner"]], on="org_code", how="left")
        data = ensure_unique_columns(data)
    indicators = get_indicator_columns(data, DEFAULT_INDICATOR_CANDIDATES)

    with st.sidebar:
        st.divider()
        st.subheader("Filters")
        consent_only = st.checkbox("Only consent=Yes", value=False)

        project_options = _ordered_project_options(data)
        selected_projects = st.multiselect("Projects", project_options, default=project_options)

        partner_options = _sorted_non_empty_options(data, "ingo_partner")
        selected_partners = st.multiselect("Partner", partner_options, default=partner_options)

        province_options = _sorted_non_empty_options(data, "province")
        selected_provinces = st.multiselect("Province", province_options, default=province_options)

        org_options = sorted(master["org_code"].dropna().astype(str).unique().tolist())
        selected_orgs = st.multiselect("Organizations", org_options, default=org_options)

    filtered = apply_filters(
        data=data,
        selected_orgs=selected_orgs,
        selected_projects=selected_projects,
        selected_partners=selected_partners,
        selected_provinces=selected_provinces,
        consent_only=consent_only,
        consent_column=indicators.get("consent"),
    )

    filtered_master = master.copy()
    if selected_orgs:
        filtered_master = filtered_master[filtered_master["org_code"].isin(selected_orgs)]
    if selected_partners:
        filtered_master = filtered_master[filtered_master["ingo_partner"].isin(selected_partners)]
    if selected_provinces:
        filtered_master = filtered_master[filtered_master["province"].isin(selected_provinces)]

    filtered_progress = build_progress_table(filtered_master, filtered)
    all_org_progress = build_progress_table(master, data)

    main_section = clickable_tabs(
        ["Public Dashboard", "Public Report", "Advanced Insights", "Organizations"],
        key="main_module_tabs",
        label="Module",
    )

    if main_section == "Public Dashboard":
        render_public_dashboard(filtered=filtered, progress=filtered_progress, template=template, theme_mode=theme_mode)

    elif main_section == "Public Report":
        render_public_report(filtered=filtered, progress=filtered_progress, indicators=indicators, theme_mode=theme_mode)

    elif main_section == "Advanced Insights":
        render_advanced_insights(
            filtered=filtered,
            progress=filtered_progress,
            indicators=indicators,
            template=template,
            theme_mode=theme_mode,
        )

    else:
        render_organization_section(
            data=data,
            master=master,
            progress=all_org_progress,
            indicators=indicators,
            correction_log=correction_log,
            sheet_url=sheet_url,
            openai_key=openai_key,
            openai_model=openai_model,
            service_info=service_info,
            template=template,
            theme_mode=theme_mode,
            forms_dir=forms_dir,
        )


if __name__ == "__main__":
    main()
