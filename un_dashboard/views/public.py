"""Public-facing dashboard and report views."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from un_dashboard.core.constants import EXPECTED_TOTAL_ORGS, ORG_SHEET_TABS, TARGET_INTERVIEWS_PER_ORG
from un_dashboard.design import (
    ThemeMode,
    chart_palette_for,
    chart_scale_for,
    clickable_tabs,
    render_glass_list,
    render_glass_stats,
    render_report_hero,
    section_heading,
    style_plotly_figure,
)
from un_dashboard.services.reporting import build_report_artifacts
from un_dashboard.services.transforms import (
    build_daily_interviews,
    build_partner_province_matrix,
    format_percent,
    top_orgs_by_progress,
)


def render_public_dashboard(
    filtered: pd.DataFrame,
    progress: pd.DataFrame,
    template: str,
    theme_mode: ThemeMode,
) -> None:
    palette = chart_palette_for(theme_mode)
    total_interviews = int(len(filtered))
    if "sheet_name" in filtered.columns:
        active_projects = int(filtered["sheet_name"].dropna().astype(str).nunique()) if not filtered.empty else 0
        loaded_projects = {str(x).strip() for x in filtered["sheet_name"].dropna().astype(str).tolist() if str(x).strip()}
        designed_count = int(len([x for x in ORG_SHEET_TABS if x in loaded_projects]))
    else:
        active_projects = int(filtered["org_code"].nunique()) if not filtered.empty else 0
        designed_count = int(progress["is_designed"].sum()) if not progress.empty else 0

    target_total = int(pd.to_numeric(progress["target"], errors="coerce").fillna(0).sum()) if not progress.empty else EXPECTED_TOTAL_ORGS * TARGET_INTERVIEWS_PER_ORG
    completion = total_interviews / target_total if target_total else np.nan

    with st.container():
        section_heading("Public KPI", "High-level indicators for current filtered scope.")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Interviews", f"{total_interviews:,}")
        col2.metric("Active Projects", f"{active_projects:,}")
        col3.metric("Designed Projects", f"{designed_count}/{len(ORG_SHEET_TABS)}")
        col4.metric("Overall Progress", format_percent(completion))

    if progress.empty:
        st.info("No data available for the selected filters.")
        return

    with st.container():
        section_heading("Organization Progress", "Interview volume compared with per-org target.")
        fig = px.bar(
            progress.sort_values("interviews", ascending=False),
            x="org_code",
            y="interviews",
            color="ingo_partner",
            title="",
            color_discrete_sequence=palette,
            template=template,
        )
        fig.add_hline(y=TARGET_INTERVIEWS_PER_ORG, line_dash="dash", line_color=palette[1])
        fig.update_layout(legend_title_text="INGO Partner", margin=dict(l=10, r=10, t=20, b=20))
        style_plotly_figure(fig, theme_mode)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        section_heading("Progress Table", "Compact organization performance matrix.")
        st.dataframe(
            progress[["org_code", "province", "ingo_partner", "interviews", "target", "progress_pct", "status"]],
            use_container_width=True,
            hide_index=True,
        )


def render_public_report(
    filtered: pd.DataFrame,
    progress: pd.DataFrame,
    indicators: dict[str, str | None],
    theme_mode: ThemeMode,
) -> None:
    with st.container():
        if filtered.empty:
            st.info("No records are available for the current filters.")
            return

        artifacts = build_report_artifacts(
            scope_kind="public",
            scope_label="Filtered public scope",
            data=filtered,
            progress=progress,
            indicators=indicators,
            theme_mode=theme_mode,
        )

        metric_map = {row["Metric"]: row["Value"] for _, row in artifacts["summary_table"].iterrows()}
        render_report_hero(
            title="Public Report Intelligence Center",
            subtitle="Advanced public reporting with narrative analysis, portfolio-wide visuals, and per-organization start-date activity intelligence.",
            badges=["PDF", "Word", "Excel", "Start-Date Analytics"],
        )
        render_glass_stats(
            [
                {"label": "Interviews", "value": metric_map.get("Interviews analyzed", "0"), "note": "Filtered public dataset"},
                {"label": "Completion", "value": metric_map.get("Completion", "N/A"), "note": "Against active target baseline"},
                {"label": "Organizations", "value": metric_map.get("Organizations covered", "0"), "note": "Distinct organizations in scope"},
                {"label": "Partners", "value": metric_map.get("Partners covered", "0"), "note": "Distinct INGO partners represented"},
            ]
        )

        info_col, risk_col, rec_col = st.columns(3)
        with info_col:
            render_glass_list("Executive Summary", artifacts["insights"])
        with risk_col:
            render_glass_list("Key Risks", artifacts["risks"])
        with rec_col:
            render_glass_list("Recommendations", artifacts["recommendations"])

        st.dataframe(artifacts["indicator_table"], use_container_width=True, hide_index=True)

        section_heading("Core Analytical Visuals", "Portfolio-wide charts included in the downloadable report package.")
        for chart in artifacts["charts"]:
            st.markdown(f"##### {chart['title']}")
            st.caption(chart["caption"])
            st.image(chart["image"], use_container_width=True)
            st.dataframe(chart["table"].head(20), use_container_width=True, hide_index=True)

        org_sections = artifacts.get("org_activity_sections", [])
        if org_sections:
            section_heading(
                "Organization Start-Date Activity",
                "Modern daily interview chart for each organization based on the `start` column.",
            )
            org_options = [section["org_code"] for section in org_sections]
            selected_org = clickable_tabs(
                org_options,
                key="public_report_org_activity",
                label="Preview organization timeline",
            )
            selected_section = next((section for section in org_sections if section["org_code"] == selected_org), org_sections[0])
            st.markdown(f"##### {selected_section['title']}")
            st.caption(selected_section["caption"])
            st.image(selected_section["image"], use_container_width=True)
            st.dataframe(selected_section["table"].head(31), use_container_width=True, hide_index=True)

        section_heading("Download Package", "Export the complete advanced report in the required format.")
        download_cols = st.columns(3)
        download_cols[0].download_button(
            "Download PDF Report",
            data=artifacts["pdf_bytes"],
            file_name=f"{artifacts['file_stub']}.pdf",
            mime="application/pdf",
        )
        download_cols[1].download_button(
            "Download Word Report",
            data=artifacts["word_bytes"],
            file_name=f"{artifacts['file_stub']}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        download_cols[2].download_button(
            "Download Excel Report",
            data=artifacts["excel_bytes"],
            file_name=f"{artifacts['file_stub']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


def render_advanced_insights(
    filtered: pd.DataFrame,
    progress: pd.DataFrame,
    indicators: dict[str, str | None],
    template: str,
    theme_mode: ThemeMode,
) -> None:
    palette = chart_palette_for(theme_mode)
    scale = chart_scale_for(theme_mode)
    with st.container():
        section_heading("Advanced Insights", "Trend, concentration map, and top performance highlights.")

        trend = build_daily_interviews(filtered, indicators.get("date"))
        left, right = st.columns((2, 1))

        with left:
            if trend.empty:
                st.info("No valid date field found for trend analysis.")
            else:
                fig_trend = px.area(
                    trend,
                    x="date",
                    y="cumulative",
                    title="Cumulative Interview Trend",
                    markers=True,
                    template=template,
                    color_discrete_sequence=[palette[1]],
                )
                fig_trend.update_layout(margin=dict(l=10, r=10, t=50, b=20))
                style_plotly_figure(fig_trend, theme_mode)
                st.plotly_chart(fig_trend, use_container_width=True)

        with right:
            top_orgs = top_orgs_by_progress(progress, limit=7)
            if top_orgs.empty:
                st.info("No organization progress data available.")
            else:
                st.dataframe(top_orgs, use_container_width=True, hide_index=True)

    matrix = build_partner_province_matrix(filtered)
    if matrix.empty:
        st.info("Not enough data for partner/province distribution matrix.")
        return

    with st.container():
        section_heading("Partner x Province", "Interview concentration heatmap.")
        melted = matrix.melt(id_vars=["ingo_partner"], var_name="province", value_name="interviews")
        heatmap = px.density_heatmap(
            melted,
            x="province",
            y="ingo_partner",
            z="interviews",
            histfunc="sum",
            color_continuous_scale=scale,
            title="",
            template=template,
        )
        heatmap.update_layout(margin=dict(l=10, r=10, t=20, b=20))
        style_plotly_figure(heatmap, theme_mode)
        st.plotly_chart(heatmap, use_container_width=True)
