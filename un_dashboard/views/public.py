"""Public-facing dashboard and report views."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from un_dashboard.core.constants import (
    EXPECTED_TOTAL_ORGS,
    ORG_SHEET_TABS,
    POSITIVE_VALUES,
    TARGET_INTERVIEWS_PER_ORG,
    YES_VALUES,
)
from un_dashboard.design import ThemeMode, chart_palette_for, chart_scale_for, section_heading, style_plotly_figure
from un_dashboard.services.exporter import to_excel_bytes
from un_dashboard.services.transforms import (
    build_daily_interviews,
    build_partner_province_matrix,
    format_percent,
    sanitize_for_display,
    score_positive_rate,
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
    else:
        active_projects = int(filtered["org_code"].nunique()) if not filtered.empty else 0
    if "sheet_name" in filtered.columns:
        loaded_projects = {str(x).strip() for x in filtered["sheet_name"].dropna().astype(str).tolist() if str(x).strip()}
        designed_count = int(len([x for x in ORG_SHEET_TABS if x in loaded_projects]))
    else:
        designed_count = int(progress["is_designed"].sum()) if not progress.empty else 0
    target_total = EXPECTED_TOTAL_ORGS * TARGET_INTERVIEWS_PER_ORG
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
) -> None:
    helpful_rate = (
        score_positive_rate(filtered[indicators["helpful"]], POSITIVE_VALUES)
        if indicators["helpful"] and indicators["helpful"] in filtered.columns
        else float("nan")
    )
    training_rate = (
        score_positive_rate(filtered[indicators["training"]], YES_VALUES)
        if indicators["training"] and indicators["training"] in filtered.columns
        else float("nan")
    )
    complaint_rate = (
        score_positive_rate(filtered[indicators["complaint_awareness"]], YES_VALUES)
        if indicators["complaint_awareness"] and indicators["complaint_awareness"] in filtered.columns
        else float("nan")
    )

    with st.container():
        section_heading("Public Report Summary", "Calculated indicators for filtered dataset.")
        st.write(f"- Interviews analyzed: **{len(filtered)}** / **{EXPECTED_TOTAL_ORGS * TARGET_INTERVIEWS_PER_ORG}**")
        st.write(f"- Training attendance (Yes): **{format_percent(training_rate)}**")
        st.write(f"- Helpfulness (Yes/Partly): **{format_percent(helpful_rate)}**")
        st.write(f"- Complaint awareness (Yes): **{format_percent(complaint_rate)}**")

        st.download_button(
            "Download Public Report (Excel)",
            data=to_excel_bytes(
                {
                    "public_report": progress,
                    "filtered_data": sanitize_for_display(filtered).head(2000),
                }
            ),
            file_name="un_women_public_report.xlsx",
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
