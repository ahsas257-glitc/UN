
"""Organization dashboard tabs for GWO beneficiaries questionnaire."""

from __future__ import annotations

import re
from typing import Mapping, Optional, Sequence

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from un_dashboard.core.constants import YES_VALUES
from un_dashboard.design import (
    ThemeMode,
    chart_palette_for,
    chart_scale_for,
    section_heading,
    style_plotly_figure,
)
from un_dashboard.services.transforms import find_column, normalize_token


def _resolve_columns(df: pd.DataFrame, candidates_map: Mapping[str, Sequence[str]]) -> dict[str, Optional[str]]:
    return {key: find_column(df, candidates) for key, candidates in candidates_map.items()}


def _parse_numeric_cell(value) -> float:
    if pd.isna(value):
        return float("nan")

    text = str(value).strip()
    if not text:
        return float("nan")

    text = text.replace(",", "")
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    if not numbers:
        return float("nan")

    nums = [float(n) for n in numbers]
    if len(nums) >= 2 and ("-" in text or "to" in text.lower()):
        return float(np.mean(nums[:2]))
    return float(nums[0])


def _numeric_series(series: pd.Series) -> pd.Series:
    return series.map(_parse_numeric_cell)


def _safe_counts(series: pd.Series, top_n: Optional[int] = None) -> pd.DataFrame:
    counts = series.fillna("Unknown").astype(str).value_counts().reset_index()
    counts.columns = ["value", "count"]
    if top_n is not None:
        counts = counts.head(top_n)
    return counts


def _multiselect_counts(series: pd.Series, top_n: int = 12) -> pd.DataFrame:
    if series is None:
        return pd.DataFrame(columns=["value", "count"])

    token_series = (
        series.dropna()
        .astype(str)
        .str.strip()
        .replace("", np.nan)
        .dropna()
        .str.split(r"\s+")
    )
    if token_series.empty:
        return pd.DataFrame(columns=["value", "count"])

    exploded = token_series.explode().dropna().astype(str).str.strip()
    if exploded.empty:
        return pd.DataFrame(columns=["value", "count"])

    counts = exploded.value_counts().reset_index()
    counts.columns = ["value", "count"]
    counts["value"] = counts["value"].str.replace("_", " ", regex=False).str.title()
    return counts.head(top_n)


def _yes_mask(series: pd.Series) -> pd.Series:
    return series.fillna("").map(normalize_token).isin(YES_VALUES)


def _yes_rate(series: pd.Series) -> float:
    if series is None or series.empty:
        return float("nan")
    valid = series.dropna()
    if valid.empty:
        return float("nan")
    return float(_yes_mask(valid).mean())


def _non_empty_rate(series: pd.Series) -> float:
    if series is None or series.empty:
        return float("nan")
    filled = series.fillna("").astype(str).str.strip()
    return float((filled != "").mean())


def _format_pct(value: float) -> str:
    if pd.isna(value):
        return "—"
    return f"{value * 100:.1f}%"


def _render_not_found(message: str) -> None:
    st.info(message)


def _build_training_combined_chart(train_df: pd.DataFrame, template: str, theme_mode: ThemeMode):
    combo = (
        train_df.groupby(["attended", "sessions_cat", "duration_cat"], dropna=False)
        .size()
        .reset_index(name="respondents")
    )
    fig = px.scatter(
        combo,
        x="sessions_cat",
        y="duration_cat",
        color="attended",
        size="respondents",
        size_max=40,
        symbol="attended",
        template=template,
        title="Combined View: Attendance + Sessions + Duration",
    )
    fig.update_layout(xaxis_title="Sessions attended", yaxis_title="Training duration")
    style_plotly_figure(fig, theme_mode)
    return fig


def _render_sample_tab(org_data: pd.DataFrame, sample_cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    continuous_scale = chart_scale_for(theme_mode)
    surveyor_col = sample_cols.get("surveyor")
    province_col = sample_cols.get("province")
    district_col = sample_cols.get("district")

    with st.container():
        section_heading("Sample Information", "Enumerator and location profile in a clean overview.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Interviews", f"{len(org_data):,}")
        c2.metric("Surveyors", f"{org_data[surveyor_col].nunique() if surveyor_col else 0:,}")
        c3.metric("Districts", f"{org_data[district_col].nunique() if district_col else 0:,}")

    with st.container():
        section_heading("Field Distribution", "Top district volume by province")
        if province_col and district_col:
            dist_df = (
                org_data[[province_col, district_col]]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index(name="interviews")
                .sort_values("interviews", ascending=False)
                .head(20)
            )
            fig = px.bar(
                dist_df,
                x="interviews",
                y=district_col,
                color=province_col,
                orientation="h",
                template=template,
                title="Top Districts by Interview Volume",
            )
            fig.update_layout(xaxis_title="Interviews", yaxis_title="District")
            style_plotly_figure(fig, theme_mode)
            st.plotly_chart(fig, use_container_width=True)
        elif surveyor_col:
            counts = _safe_counts(org_data[surveyor_col], top_n=15)
            fig = px.bar(
                counts,
                x="count",
                y="value",
                color="count",
                color_continuous_scale=continuous_scale,
                template=template,
                orientation="h",
                title="Top Surveyors by Interview Volume",
            )
            fig.update_layout(showlegend=False, xaxis_title="Interviews", yaxis_title="Surveyor")
            style_plotly_figure(fig, theme_mode)
            st.plotly_chart(fig, use_container_width=True)
        else:
            _render_not_found("Sample location columns are not available.")

    with st.container():
        section_heading("Sample Table", "Compact data preview")
        preview_cols = [c for c in [surveyor_col, province_col, district_col] if c]
        if preview_cols:
            st.dataframe(org_data[preview_cols].head(300), use_container_width=True, hide_index=True)
        else:
            _render_not_found("No sample columns available for preview.")

def _render_respondent_tab(org_data: pd.DataFrame, cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    continuous_scale = chart_scale_for(theme_mode)
    cat_keys = ["age_group", "gender", "marital", "education", "employment"]
    age_col = cols.get("age_group")
    gender_col = cols.get("gender")

    with st.container():
        section_heading("Respondent Distribution", "Age-group and gender relationship")
        if age_col and gender_col:
            age_gender = (
                org_data[[age_col, gender_col]]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index(name="interviews")
            )
            fig = px.bar(
                age_gender,
                x=age_col,
                y="interviews",
                color=gender_col,
                barmode="group",
                template=template,
                title="Age Group by Gender",
            )
            fig.update_layout(xaxis_title="Age group", yaxis_title="Interview count")
            style_plotly_figure(fig, theme_mode)
            st.plotly_chart(fig, use_container_width=True)
        else:
            fallback_col = next((cols.get(k) for k in cat_keys if cols.get(k)), None)
            if fallback_col:
                counts = _safe_counts(org_data[fallback_col], top_n=15)
                fig = px.bar(
                    counts,
                    x="count",
                    y="value",
                    orientation="h",
                    template=template,
                    title=f"Distribution: {fallback_col}",
                )
                fig.update_layout(xaxis_title="Interview count", yaxis_title="Category")
                style_plotly_figure(fig, theme_mode)
                st.plotly_chart(fig, use_container_width=True)
            else:
                _render_not_found("Respondent columns are not available.")

    left, right = st.columns(2)
    with left:
        with st.container():
            section_heading("Age x Gender", "Cross-distribution heatmap")
            if age_col and gender_col:
                cross = pd.crosstab(org_data[age_col].fillna("Unknown"), org_data[gender_col].fillna("Unknown"))
                fig_hm = px.imshow(
                    cross,
                    text_auto=True,
                    color_continuous_scale=continuous_scale,
                    aspect="auto",
                    template=template,
                )
                style_plotly_figure(fig_hm, theme_mode)
                st.plotly_chart(fig_hm, use_container_width=True)
            else:
                _render_not_found("Age/Gender columns not found.")

    with right:
        with st.container():
            section_heading("Income Pattern", "Household size vs monthly income")
            hh_col = cols.get("household_members")
            income_col = cols.get("avg_income")
            emp_col = cols.get("employment")
            if hh_col and income_col:
                scatter_df = pd.DataFrame(
                    {
                        "household_members": _numeric_series(org_data[hh_col]),
                        "avg_income": _numeric_series(org_data[income_col]),
                        "employment": org_data[emp_col].fillna("Unknown").astype(str) if emp_col else "Unknown",
                    }
                ).dropna(subset=["household_members", "avg_income"])
                if not scatter_df.empty:
                    fig_sc = px.scatter(
                        scatter_df,
                        x="household_members",
                        y="avg_income",
                        color="employment",
                        size="household_members",
                        size_max=22,
                        opacity=0.78,
                        template=template,
                        title="Household Members vs Monthly Income",
                    )
                    fig_sc.update_layout(legend_title_text="Employment")
                    style_plotly_figure(fig_sc, theme_mode)
                    st.plotly_chart(fig_sc, use_container_width=True)
                else:
                    _render_not_found("Numeric values are not available for income analysis.")
            else:
                _render_not_found("Household members / income columns not found.")

    with st.container():
        section_heading("Respondent Table", "Focused preview for analysis")
        preview_cols = [cols.get(k) for k in cat_keys + ["household_members", "avg_income"]]
        preview_cols = [c for c in preview_cols if c]
        if preview_cols:
            st.dataframe(org_data[preview_cols].head(300), use_container_width=True, hide_index=True)
        else:
            _render_not_found("No respondent columns available for preview.")


def _render_training_tab(org_data: pd.DataFrame, cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    palette = chart_palette_for(theme_mode)
    attend_col = cols.get("attended_training")
    sessions_col = cols.get("sessions_attended")
    duration_col = cols.get("training_duration")

    if not attend_col and not sessions_col and not duration_col:
        _render_not_found("Training columns were not detected in this dataset.")
        return

    train_df = pd.DataFrame(index=org_data.index)
    train_df["attended"] = org_data[attend_col].fillna("Unknown").astype(str) if attend_col else "Unknown"
    train_df["sessions_cat"] = org_data[sessions_col].fillna("Unknown").astype(str) if sessions_col else "Unknown"
    train_df["duration_cat"] = org_data[duration_col].fillna("Unknown").astype(str) if duration_col else "Unknown"
    train_df["sessions_num"] = _numeric_series(org_data[sessions_col]) if sessions_col else np.nan
    train_df["duration_num"] = _numeric_series(org_data[duration_col]) if duration_col else np.nan

    with st.container():
        section_heading("Training Attendance", "Compact participation overview")
        counts = _safe_counts(train_df["attended"])
        c1, c2 = st.columns((1, 1))
        with c1:
            fig_att = px.pie(
                counts,
                names="value",
                values="count",
                hole=0.62,
                template=template,
                color_discrete_sequence=palette,
                title="Attendance Split",
            )
            style_plotly_figure(fig_att, theme_mode)
            st.plotly_chart(fig_att, use_container_width=True)
        with c2:
            summary = (
                train_df.groupby("attended", dropna=False)
                .agg(
                    interviews=("attended", "size"),
                    avg_sessions=("sessions_num", "mean"),
                    avg_duration=("duration_num", "mean"),
                )
                .reset_index()
                .round(2)
            )
            st.dataframe(summary, use_container_width=True, hide_index=True)

    with st.container():
        section_heading("Combined Training Chart", "Attendance, sessions, and duration in one chart")
        fig_combo_all = _build_training_combined_chart(train_df, template, theme_mode)
        st.plotly_chart(fig_combo_all, use_container_width=True)

    with st.container():
        section_heading("Attendance Summary", "Average sessions and duration by attendance status")
        combo = train_df.dropna(subset=["sessions_num", "duration_num"]).copy()
        if not combo.empty:
            summary_plot = (
                combo.groupby("attended", dropna=False)
                .agg(
                    avg_sessions=("sessions_num", "mean"),
                    avg_duration=("duration_num", "mean"),
                    respondents=("attended", "size"),
                )
                .reset_index()
            )
            melted = summary_plot.melt(
                id_vars=["attended", "respondents"],
                value_vars=["avg_sessions", "avg_duration"],
                var_name="metric",
                value_name="value",
            )
            fig = px.bar(
                melted,
                x="attended",
                y="value",
                color="metric",
                barmode="group",
                template=template,
                title="Average Sessions and Duration by Attendance",
            )
            fig.update_layout(xaxis_title="Attendance status", yaxis_title="Average value")
            style_plotly_figure(fig, theme_mode)
            st.plotly_chart(fig, use_container_width=True)
        else:
            _render_not_found("No numeric values available for attendance summary.")

def _render_kits_tab(org_data: pd.DataFrame, cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    palette = chart_palette_for(theme_mode)
    received_kit_col = cols.get("received_kit")
    item_specs = [
        ("Aluminum cooking pot", "aluminum_cooking_pot", "aluminum_cooking_pot_qty"),
        ("Gas stove", "gas_stove", "gas_stove_qty"),
        ("Gas cylinder", "gas_cylinder", "gas_cylinder_qty"),
        ("Glass jars", "glass_jars", "glass_jars_qty"),
        ("Knives", "knives", "knives_qty"),
        ("Plastic bucket", "plastic_bucket", "plastic_bucket_qty"),
        ("Hand mixer", "hand_mixer", "hand_mixer_qty"),
        ("Table", "table", "table_qty"),
    ]

    rows = []
    for item_label, yn_key, qty_key in item_specs:
        yn_col = cols.get(yn_key)
        qty_col = cols.get(qty_key)

        qty_series = _numeric_series(org_data[qty_col]) if qty_col else pd.Series(dtype=float)
        total_qty = float(qty_series.fillna(0).sum()) if not qty_series.empty else 0.0

        if yn_col:
            households = int(_yes_mask(org_data[yn_col]).sum())
        elif not qty_series.empty:
            households = int((qty_series.fillna(0) > 0).sum())
        else:
            households = 0

        rows.append(
            {
                "item": item_label,
                "households_reported": households,
                "total_quantity": total_qty,
            }
        )

    kit_summary = pd.DataFrame(rows).sort_values("total_quantity", ascending=False).reset_index(drop=True)

    with st.container():
        section_heading("Kit Coverage", "Single combined chart for all production-kit items")
        yes_count = int(_yes_mask(org_data[received_kit_col]).sum()) if received_kit_col else 0
        k1, k2, k3 = st.columns(3)
        k1.metric("Received kit (Yes)", f"{yes_count:,}")
        k2.metric("Total interviews", f"{len(org_data):,}")
        k3.metric("Total quantities", f"{kit_summary['total_quantity'].sum():,.0f}")

        if kit_summary["total_quantity"].sum() > 0 or kit_summary["households_reported"].sum() > 0:
            fig_kits = make_subplots(specs=[[{"secondary_y": True}]])
            fig_kits.add_trace(
                go.Bar(
                    x=kit_summary["item"],
                    y=kit_summary["total_quantity"],
                    name="Total Quantity",
                    marker_color=palette[0],
                    text=kit_summary["total_quantity"].round(0).astype(int),
                    textposition="outside",
                ),
                secondary_y=False,
            )
            fig_kits.add_trace(
                go.Scatter(
                    x=kit_summary["item"],
                    y=kit_summary["households_reported"],
                    name="Households Reporting",
                    mode="lines+markers",
                    line=dict(width=3, color=palette[1]),
                    marker=dict(size=8),
                ),
                secondary_y=True,
            )
            fig_kits.update_layout(title="Production Kit Coverage and Quantity", xaxis_title="Kit item")
            fig_kits.update_yaxes(title_text="Total quantity", secondary_y=False)
            fig_kits.update_yaxes(title_text="Households", secondary_y=True)
            style_plotly_figure(fig_kits, theme_mode)
            st.plotly_chart(fig_kits, use_container_width=True)
        else:
            _render_not_found("No kit quantity or item-level reporting detected.")

    with st.container():
        section_heading("Kit Item Table", "Compact table for item-level totals")
        st.dataframe(kit_summary, use_container_width=True, hide_index=True)


def _render_use_skills_tab(org_data: pd.DataFrame, cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    continuous_scale = chart_scale_for(theme_mode)
    producing_col = cols.get("producing_now")
    frequency_col = cols.get("produce_frequency")
    sell_col = cols.get("where_sell")
    hygiene_col = cols.get("hygiene_followed")
    hygiene_reason_col = cols.get("hygiene_not_followed_reason")

    with st.container():
        section_heading("Use of Skills and Inputs", "Production, selling channels, and hygiene implementation")
        c1, c2, c3 = st.columns(3)
        c1.metric("Producing now (Yes)", _format_pct(_yes_rate(org_data[producing_col])) if producing_col else "—")
        c2.metric("Hygiene followed (Yes)", _format_pct(_yes_rate(org_data[hygiene_col])) if hygiene_col else "—")
        c3.metric("Selling channels reported", f"{_multiselect_counts(org_data[sell_col]).shape[0]:,}" if sell_col else "0")

    left, right = st.columns(2)
    with left:
        with st.container():
            section_heading("Production Status", "Current production distribution")
            if producing_col:
                counts = _safe_counts(org_data[producing_col], top_n=10)
                fig = px.bar(
                    counts,
                    x="value",
                    y="count",
                    color="count",
                    template=template,
                    color_continuous_scale=continuous_scale,
                    title="Are beneficiaries currently producing?",
                )
                fig.update_layout(showlegend=False, xaxis_title="Status", yaxis_title="Interview count")
                style_plotly_figure(fig, theme_mode)
                st.plotly_chart(fig, use_container_width=True)
            else:
                _render_not_found("Production status column not found.")

    with right:
        with st.container():
            section_heading("Selling Channels", "Top selected locations for selling")
            if sell_col:
                sell_counts = _multiselect_counts(org_data[sell_col], top_n=12)
                if not sell_counts.empty:
                    fig = px.bar(
                        sell_counts,
                        x="count",
                        y="value",
                        orientation="h",
                        template=template,
                        color="count",
                        color_continuous_scale=continuous_scale,
                        title="Where do beneficiaries sell?",
                    )
                    fig.update_layout(showlegend=False, xaxis_title="Selections", yaxis_title="Selling channel")
                    style_plotly_figure(fig, theme_mode)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    _render_not_found("No selling channel selections were found.")
            else:
                _render_not_found("Selling channel column not found.")

    with st.container():
        section_heading("Hygiene Barriers", "Reported reasons when hygiene is not followed")
        if hygiene_reason_col:
            reasons = _multiselect_counts(org_data[hygiene_reason_col], top_n=12)
            if not reasons.empty:
                fig = px.bar(
                    reasons,
                    x="count",
                    y="value",
                    orientation="h",
                    template=template,
                    color="count",
                    color_continuous_scale=continuous_scale,
                    title="Hygiene not followed reasons",
                )
                fig.update_layout(showlegend=False, xaxis_title="Mentions", yaxis_title="Reason")
                style_plotly_figure(fig, theme_mode)
                st.plotly_chart(fig, use_container_width=True)
            else:
                _render_not_found("No hygiene barrier reasons were reported.")
        else:
            _render_not_found("Hygiene barrier column not found.")

    with st.container():
        section_heading("Skills Table", "Production and selling details preview")
        preview_cols = [c for c in [producing_col, frequency_col, sell_col, hygiene_col, hygiene_reason_col] if c]
        if preview_cols:
            st.dataframe(org_data[preview_cols].head(300), use_container_width=True, hide_index=True)

def _render_market_changes_tab(org_data: pd.DataFrame, cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    palette = chart_palette_for(theme_mode)
    continuous_scale = chart_scale_for(theme_mode)
    info_col = cols.get("info_markets")
    introduced_col = cols.get("introduced_buyers")
    helpful_col = cols.get("market_helpful")
    changes_col = cols.get("changes_helped")

    with st.container():
        section_heading("Market Linkages", "Access to market information and buyer introductions")
        c1, c2, c3 = st.columns(3)
        c1.metric("Informed on markets (Yes)", _format_pct(_yes_rate(org_data[info_col])) if info_col else "—")
        c2.metric("Introduced to buyers (Yes)", _format_pct(_yes_rate(org_data[introduced_col])) if introduced_col else "—")
        c3.metric("Helpful response present", _format_pct(_non_empty_rate(org_data[helpful_col])) if helpful_col else "—")

    with st.container():
        section_heading("Market Support Outcomes", "Distribution for key market support variables")
        chart_data = []
        for label, col in [
            ("Given market info", info_col),
            ("Introduced to buyers", introduced_col),
        ]:
            if col:
                yes_count = int(_yes_mask(org_data[col]).sum())
                total = int(org_data[col].notna().sum())
                no_count = max(total - yes_count, 0)
                chart_data.append({"metric": label, "response": "Yes", "count": yes_count})
                chart_data.append({"metric": label, "response": "No/Other", "count": no_count})

        if chart_data:
            chart_df = pd.DataFrame(chart_data)
            fig = px.bar(
                chart_df,
                x="metric",
                y="count",
                color="response",
                barmode="stack",
                template=template,
                title="Market support response distribution",
            )
            fig.update_layout(xaxis_title="Metric", yaxis_title="Interview count")
            style_plotly_figure(fig, theme_mode)
            st.plotly_chart(fig, use_container_width=True)
        else:
            _render_not_found("Market support columns were not found.")

    left, right = st.columns(2)
    with left:
        with st.container():
            section_heading("Helpfulness", "Was market support helpful?")
            if helpful_col:
                helpful_counts = _safe_counts(org_data[helpful_col], top_n=10)
                fig = px.pie(
                    helpful_counts,
                    names="value",
                    values="count",
                    hole=0.6,
                    template=template,
                    title="Helpfulness distribution",
                    color_discrete_sequence=palette,
                )
                style_plotly_figure(fig, theme_mode)
                st.plotly_chart(fig, use_container_width=True)
            else:
                _render_not_found("Helpfulness column not found.")

    with right:
        with st.container():
            section_heading("Perceived Changes", "Top reported changes from the intervention")
            if changes_col:
                changes_counts = _multiselect_counts(org_data[changes_col], top_n=12)
                if not changes_counts.empty:
                    fig = px.bar(
                        changes_counts,
                        x="count",
                        y="value",
                        orientation="h",
                        template=template,
                        color="count",
                        color_continuous_scale=continuous_scale,
                        title="Most reported perceived changes",
                    )
                    fig.update_layout(showlegend=False, xaxis_title="Mentions", yaxis_title="Change category")
                    style_plotly_figure(fig, theme_mode)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    _render_not_found("No perceived changes were reported.")
            else:
                _render_not_found("Perceived changes column not found.")


def _render_safeguarding_tab(org_data: pd.DataFrame, cols: dict[str, Optional[str]], template: str, theme_mode: ThemeMode) -> None:
    continuous_scale = chart_scale_for(theme_mode)
    family_col = cols.get("family_support")
    informed_col = cols.get("informed_concerns")
    know_contact_col = cols.get("know_contact")
    concerns_col = cols.get("concerns_family")

    with st.container():
        section_heading("Household and Safeguarding", "Support and awareness indicators for accountability and protection")
        c1, c2, c3 = st.columns(3)
        c1.metric("Family support (Yes)", _format_pct(_yes_rate(org_data[family_col])) if family_col else "—")
        c2.metric("Informed on concerns (Yes)", _format_pct(_yes_rate(org_data[informed_col])) if informed_col else "—")
        c3.metric("Know complaint contact (Yes)", _format_pct(_yes_rate(org_data[know_contact_col])) if know_contact_col else "—")

    left, right = st.columns(2)
    with left:
        with st.container():
            section_heading("Support Profile", "Distribution of household support")
            if family_col:
                counts = _safe_counts(org_data[family_col], top_n=10)
                fig = px.bar(
                    counts,
                    x="value",
                    y="count",
                    template=template,
                    color="count",
                    color_continuous_scale=continuous_scale,
                    title="Family support distribution",
                )
                fig.update_layout(showlegend=False, xaxis_title="Response", yaxis_title="Interview count")
                style_plotly_figure(fig, theme_mode)
                st.plotly_chart(fig, use_container_width=True)
            else:
                _render_not_found("Family support column not found.")

    with right:
        with st.container():
            section_heading("Awareness Cross-Check", "Informed on concerns vs knowledge of contact")
            if informed_col and know_contact_col:
                cross = pd.crosstab(
                    org_data[informed_col].fillna("Unknown"),
                    org_data[know_contact_col].fillna("Unknown"),
                )
                fig = px.imshow(
                    cross,
                    text_auto=True,
                    color_continuous_scale=continuous_scale,
                    aspect="auto",
                    template=template,
                    title="Safeguarding awareness matrix",
                )
                style_plotly_figure(fig, theme_mode)
                st.plotly_chart(fig, use_container_width=True)
            else:
                _render_not_found("Safeguarding awareness columns not found.")

    with st.container():
        section_heading("Concerns Notes", "Open-ended concern reporting and data preview")
        if concerns_col:
            non_empty = int(org_data[concerns_col].fillna("").astype(str).str.strip().ne("").sum())
            rate = non_empty / len(org_data) if len(org_data) else float("nan")
            st.metric("Rows with concern text", f"{non_empty:,} ({_format_pct(rate)})")
            preview = org_data[[concerns_col]].copy()
            preview.columns = ["concerns_note"]
            st.dataframe(preview.head(200), use_container_width=True, hide_index=True)
        else:
            _render_not_found("Open-ended concerns column not found.")


def render_gwo_dashboard(
    org_data: pd.DataFrame,
    tab_config: Mapping[str, Mapping[str, Sequence[str]]],
    template: str,
    theme_mode: ThemeMode,
) -> None:
    if org_data.empty:
        st.info("No data found for this organization.")
        return

    sample_cols = _resolve_columns(org_data, tab_config.get("sample_information", {}))
    respondent_cols = _resolve_columns(org_data, tab_config.get("respondent_details", {}))
    training_cols = _resolve_columns(org_data, tab_config.get("participation_training", {}))
    kits_cols = _resolve_columns(org_data, tab_config.get("receipt_production_kits", {}))
    skills_cols = _resolve_columns(org_data, tab_config.get("use_skills_inputs", {}))
    market_cols = _resolve_columns(org_data, tab_config.get("market_perceived_changes", {}))
    safeguarding_cols = _resolve_columns(org_data, tab_config.get("household_safeguarding", {}))

    (
        tab_sample,
        tab_resp,
        tab_train,
        tab_kits,
        tab_skills,
        tab_market,
        tab_safe,
    ) = st.tabs(
        [
            "Sample Information",
            "Respondent details",
            "Participation in training",
            "Receipt of production kits",
            "Use of skills and inputs",
            "Market and perceived changes",
            "Household and safeguarding",
        ]
    )

    with tab_sample:
        _render_sample_tab(org_data, sample_cols, template, theme_mode)

    with tab_resp:
        _render_respondent_tab(org_data, respondent_cols, template, theme_mode)

    with tab_train:
        _render_training_tab(org_data, training_cols, template, theme_mode)

    with tab_kits:
        _render_kits_tab(org_data, kits_cols, template, theme_mode)

    with tab_skills:
        _render_use_skills_tab(org_data, skills_cols, template, theme_mode)

    with tab_market:
        _render_market_changes_tab(org_data, market_cols, template, theme_mode)

    with tab_safe:
        _render_safeguarding_tab(org_data, safeguarding_cols, template, theme_mode)
