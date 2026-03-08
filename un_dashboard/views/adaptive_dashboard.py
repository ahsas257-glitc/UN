"""Adaptive dashboard renderer for questionnaire-driven organization views."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from un_dashboard.design import ThemeMode, chart_palette_for, chart_scale_for, clickable_tabs, section_heading, style_plotly_figure
from un_dashboard.questionnaires.base import QuestionnaireSchema
from un_dashboard.services.form_profiles import resolve_profile
from un_dashboard.services.transforms import find_column


def _safe_id(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", str(text or "")).strip("_").lower() or "x"


def _series(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(dtype="object")
    selected = df[column]
    if isinstance(selected, pd.DataFrame):
        if selected.shape[1] == 0:
            return pd.Series(dtype="object")
        return selected.iloc[:, 0]
    return selected


def _to_numeric(series: pd.Series) -> pd.Series:
    clean = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(clean, errors="coerce")


def _is_numeric_like(series: pd.Series, threshold: float = 0.75) -> bool:
    if series.empty:
        return False
    if pd.api.types.is_numeric_dtype(series):
        return True
    sample = series.dropna().astype(str).head(500)
    if sample.empty:
        return False
    return bool(_to_numeric(sample).notna().mean() >= threshold)


def _value_counts(series: pd.Series, limit: int = 20) -> pd.DataFrame:
    return (
        series.fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts(dropna=False)
        .head(limit)
        .rename_axis("value")
        .reset_index(name="count")
    )


def _multi_counts(series: pd.Series, limit: int = 25) -> pd.DataFrame:
    non_empty = series.dropna().map(str).map(lambda x: x.strip())
    non_empty = non_empty[non_empty != ""]
    if non_empty.empty:
        return pd.DataFrame(columns=["value", "count"])

    exploded = non_empty.str.split(r"\s+").explode().dropna().astype(str).str.strip()
    exploded = exploded[exploded != ""]
    if exploded.empty:
        return pd.DataFrame(columns=["value", "count"])

    out = exploded.value_counts().head(limit).rename_axis("value").reset_index(name="count")
    out["value"] = out["value"].str.replace("_", " ", regex=False).str.title()
    return out


def _safe_preview(df: pd.DataFrame, columns: list[str], limit: int = 300) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for col in columns:
        out[col] = _series(df, col)
    return out.head(limit)


def _tab_title_from_key(tab_key: str) -> str:
    text = str(tab_key or "").replace("_", " ").strip()
    return text.title() if text else "General"


def _build_tabs_from_questionnaire(
    org_data: pd.DataFrame,
    questionnaire: QuestionnaireSchema,
) -> tuple[list[dict], list[dict]]:
    tabs: list[dict] = []
    all_questions: list[dict] = []
    seen_cols: set[str] = set()

    tab_label_map = dict(questionnaire.org_dashboard_tab_labels or {})
    for tab_key, field_map in questionnaire.org_dashboard_tabs.items():
        tab_questions: list[dict] = []
        for field_key, candidates in (field_map or {}).items():
            candidate_list = [str(x).strip() for x in (candidates or []) if str(x).strip()]
            if not candidate_list:
                continue
            matched_col = find_column(org_data, candidate_list)
            if not matched_col or matched_col in seen_cols:
                continue
            seen_cols.add(matched_col)

            label = candidate_list[0]
            if label.lower() == str(matched_col).strip().lower():
                label = str(field_key).replace("_", " ").strip().title()

            question = {
                "name": str(matched_col),
                "label": label or str(matched_col),
                "type": "unknown",
                "is_multi": False,
                "group_path": [],
            }
            tab_questions.append(question)
            all_questions.append(question)

        if tab_questions:
            tabs.append(
                {
                    "key": str(tab_key),
                    "label": tab_label_map.get(str(tab_key), _tab_title_from_key(str(tab_key))),
                    "questions": tab_questions,
                }
            )

    return tabs, all_questions


def _question_completion_df(data: pd.DataFrame, questions: list[dict]) -> pd.DataFrame:
    rows: list[dict] = []
    n = len(data)
    if n == 0:
        return pd.DataFrame(columns=["question", "label", "filled", "fill_rate"])

    for q in questions:
        name = str(q.get("name", ""))
        if not name or name not in data.columns:
            continue
        s = _series(data, name)
        filled = int(s.fillna("").astype(str).str.strip().ne("").sum())
        rows.append(
            {
                "question": name,
                "label": str(q.get("label") or name),
                "filled": filled,
                "fill_rate": float(filled / n),
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["fill_rate", "filled"], ascending=[False, False]).reset_index(drop=True)


def _render_single_question(
    data: pd.DataFrame,
    question: dict,
    breakdown_col: str | None,
    template: str,
    theme_mode: ThemeMode,
    key: str,
) -> None:
    palette = chart_palette_for(theme_mode)
    scale = chart_scale_for(theme_mode)

    col_name = str(question["name"])
    label = str(question.get("label") or col_name)
    series = _series(data, col_name)
    if series.empty:
        st.info("Selected question is not available in this dataset.")
        return

    non_empty = series.fillna("").astype(str).str.strip().replace("", pd.NA).dropna()
    total_rows = int(len(series))
    valid_rows = int(non_empty.shape[0])
    missing_rows = max(total_rows - valid_rows, 0)
    unique_count = int(non_empty.nunique()) if valid_rows else 0

    k1, k2, k3 = st.columns(3)
    k1.metric("Answered", f"{valid_rows:,}")
    k2.metric("Missing", f"{missing_rows:,}")
    k3.metric("Unique values", f"{unique_count:,}")

    is_multi = bool(question.get("is_multi"))
    is_numeric = _is_numeric_like(series)

    if is_multi:
        chart_df = _multi_counts(series)
        if chart_df.empty:
            st.info("No multi-select options detected for this question.")
            return
        fig = px.bar(
            chart_df,
            x="count",
            y="value",
            orientation="h",
            template=template,
            color="count",
            color_continuous_scale=scale,
            title=label,
        )
        fig.update_layout(showlegend=False, xaxis_title="Mentions", yaxis_title="Options")
        style_plotly_figure(fig, theme_mode)
        st.plotly_chart(fig, use_container_width=True, key=f"{key}_multi")
        st.dataframe(chart_df, use_container_width=True, hide_index=True)
        return

    if is_numeric:
        numeric = _to_numeric(series)
        stats = numeric.describe(percentiles=[0.25, 0.5, 0.75]).dropna()
        if not stats.empty:
            st.caption(
                f"Min: {stats.get('min', np.nan):.2f} | Median: {stats.get('50%', np.nan):.2f} | "
                f"Mean: {stats.get('mean', np.nan):.2f} | Max: {stats.get('max', np.nan):.2f}"
            )

        if breakdown_col and breakdown_col != "None":
            breakdown = _series(data, breakdown_col).fillna("Unknown").astype(str)
            plot_df = pd.DataFrame({"value": numeric, "group": breakdown}).dropna(subset=["value"])
            if plot_df.empty:
                st.info("No numeric values available for this question.")
                return
            top_groups = plot_df["group"].value_counts().head(12).index
            plot_df = plot_df[plot_df["group"].isin(top_groups)]
            fig = px.box(
                plot_df,
                x="group",
                y="value",
                template=template,
                color="group",
                title=label,
            )
            fig.update_layout(showlegend=False, xaxis_title=breakdown_col, yaxis_title="Value")
        else:
            plot_df = pd.DataFrame({"value": numeric}).dropna(subset=["value"])
            if plot_df.empty:
                st.info("No numeric values available for this question.")
                return
            fig = px.histogram(
                plot_df,
                x="value",
                nbins=40,
                template=template,
                color_discrete_sequence=[palette[0]],
                title=label,
            )
            fig.update_layout(xaxis_title="Value", yaxis_title="Count")

        style_plotly_figure(fig, theme_mode)
        st.plotly_chart(fig, use_container_width=True, key=f"{key}_num")

        preview = pd.DataFrame({col_name: series})
        if breakdown_col and breakdown_col != "None":
            preview[breakdown_col] = _series(data, breakdown_col)
        st.dataframe(preview.head(300), use_container_width=True, hide_index=True)
        return

    if breakdown_col and breakdown_col != "None" and breakdown_col != col_name:
        x_vals = series.fillna("Unknown").astype(str)
        y_vals = _series(data, breakdown_col).fillna("Unknown").astype(str)
        ctab = pd.crosstab(x_vals, y_vals)
        if ctab.empty:
            st.info("No data available for this cross analysis.")
            return
        if ctab.shape[0] > 20:
            ctab = ctab.head(20)
        if ctab.shape[1] > 20:
            ctab = ctab.iloc[:, :20]

        fig = px.imshow(
            ctab,
            text_auto=True,
            aspect="auto",
            template=template,
            color_continuous_scale=scale,
            title=label,
        )
        style_plotly_figure(fig, theme_mode)
        st.plotly_chart(fig, use_container_width=True, key=f"{key}_ctab")
        st.dataframe(ctab.reset_index(), use_container_width=True, hide_index=True)
        return

    chart_df = _value_counts(series)
    fig = px.bar(
        chart_df,
        x="value",
        y="count",
        template=template,
        color="count",
        color_continuous_scale=scale,
        title=label,
    )
    fig.update_layout(showlegend=False, xaxis_title="Response", yaxis_title="Count")
    style_plotly_figure(fig, theme_mode)
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_cat")
    st.dataframe(chart_df, use_container_width=True, hide_index=True)


def _render_cross_analysis(
    data: pd.DataFrame,
    all_questions: list[dict],
    template: str,
    theme_mode: ThemeMode,
    key: str,
) -> None:
    section_heading("Cross Analysis", "Compare any two questions instantly.")
    valid_questions = [q for q in all_questions if str(q.get("name", "")) in data.columns]
    if len(valid_questions) < 2:
        st.info("Need at least two questions for cross analysis.")
        return

    cols = [str(q["name"]) for q in valid_questions]

    c1, c2, c3 = st.columns(3)
    x_col = c1.selectbox("X", cols, key=f"{key}_x")
    y_col = c2.selectbox("Y", cols, index=min(1, len(cols) - 1), key=f"{key}_y")
    color_col = c3.selectbox("Color (optional)", ["None"] + cols, key=f"{key}_color")

    x_series = _series(data, x_col)
    y_series = _series(data, y_col)
    x_num = _is_numeric_like(x_series)
    y_num = _is_numeric_like(y_series)
    color_arg = None if color_col == "None" else color_col

    if x_num and y_num:
        plot_df = pd.DataFrame({x_col: _to_numeric(x_series), y_col: _to_numeric(y_series)}).dropna(subset=[x_col, y_col])
        if color_arg:
            plot_df[color_arg] = _series(data, color_arg).astype(str)
        if plot_df.empty:
            st.info("No numeric rows available for this combination.")
            return
        fig = px.scatter(plot_df, x=x_col, y=y_col, color=color_arg, template=template, title="Cross Analysis")
    elif x_num and not y_num:
        plot_df = pd.DataFrame({x_col: _to_numeric(x_series), y_col: y_series.astype(str)}).dropna(subset=[x_col])
        if plot_df.empty:
            st.info("No rows available for this combination.")
            return
        top_cat = plot_df[y_col].value_counts().head(15).index
        plot_df = plot_df[plot_df[y_col].isin(top_cat)]
        fig = px.box(plot_df, x=y_col, y=x_col, template=template, title="Cross Analysis")
    elif not x_num and y_num:
        plot_df = pd.DataFrame({x_col: x_series.astype(str), y_col: _to_numeric(y_series)}).dropna(subset=[y_col])
        if plot_df.empty:
            st.info("No rows available for this combination.")
            return
        top_cat = plot_df[x_col].value_counts().head(15).index
        plot_df = plot_df[plot_df[x_col].isin(top_cat)]
        fig = px.box(plot_df, x=x_col, y=y_col, template=template, title="Cross Analysis")
    else:
        ctab = pd.crosstab(x_series.fillna("Unknown").astype(str), y_series.fillna("Unknown").astype(str))
        if ctab.empty:
            st.info("No rows available for this combination.")
            return
        if ctab.shape[0] > 20:
            ctab = ctab.head(20)
        if ctab.shape[1] > 20:
            ctab = ctab.iloc[:, :20]
        fig = px.imshow(
            ctab,
            text_auto=True,
            aspect="auto",
            template=template,
            color_continuous_scale=chart_scale_for(theme_mode),
            title="Cross Analysis",
        )

    style_plotly_figure(fig, theme_mode)
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_plot")


def render_adaptive_dashboard(
    org_data: pd.DataFrame,
    project_name: str,
    forms_dir: str,
    template: str,
    theme_mode: ThemeMode,
    questionnaire: QuestionnaireSchema | None = None,
) -> None:
    if org_data.empty:
        st.info("No data found for this organization/project.")
        return

    if questionnaire and questionnaire.org_dashboard_tabs:
        tabs_conf, all_questions = _build_tabs_from_questionnaire(org_data, questionnaire)
    else:
        profile = resolve_profile(project_name, org_data.columns.tolist(), forms_dir)
        tabs_conf = profile.get("tabs", [])
        all_questions = [q for q in profile.get("questions", []) if str(q.get("name", "")) in org_data.columns]

    if not tabs_conf or not all_questions:
        st.info("No questionnaire mapping found for this project.")
        return

    available_tabs: list[dict] = []
    for tab in tabs_conf:
        questions = [q for q in tab.get("questions", []) if str(q.get("name", "")) in org_data.columns]
        if questions:
            if str(tab.get("label", "")).strip().lower() == "general" and len(questions) <= 1:
                continue
            available_tabs.append({"key": tab.get("key", "general"), "label": tab.get("label", "General"), "questions": questions})

    if not available_tabs:
        st.info("No mapped fields were found in this dataset.")
        return

    tab_labels = [str(t["label"]) for t in available_tabs] + ["Cross Analysis"]
    selected_tab = clickable_tabs(
        tab_labels,
        key=f"adaptive_section_{_safe_id(project_name)}",
        label="Questionnaire section",
    )

    if selected_tab == "Cross Analysis":
        _render_cross_analysis(
            data=org_data,
            all_questions=all_questions,
            template=template,
            theme_mode=theme_mode,
            key=f"cross_{_safe_id(project_name)}",
        )
        return

    tab = next((item for item in available_tabs if str(item["label"]) == selected_tab), available_tabs[0])
    tab_key = _safe_id(f"{project_name}_{tab['key']}")
    questions = tab["questions"]

    section_heading(str(tab["label"]), "Section generated directly from XLSForm group structure.")

    completion = _question_completion_df(org_data, questions)
    avg_fill = float(completion["fill_rate"].mean()) if not completion.empty else float("nan")

    m1, m2, m3 = st.columns(3)
    m1.metric("Rows", f"{len(org_data):,}")
    m2.metric("Questions", f"{len(questions):,}")
    m3.metric("Avg completion", "—" if pd.isna(avg_fill) else f"{avg_fill * 100:.1f}%")

    if not completion.empty:
        comp_top = completion.head(14).copy()
        fig_comp = px.bar(
            comp_top,
            x="fill_rate",
            y="label",
            orientation="h",
            template=template,
            color="fill_rate",
            color_continuous_scale=chart_scale_for(theme_mode),
            title="Question Completion Rate",
        )
        fig_comp.update_layout(showlegend=False, xaxis_title="Completion rate", yaxis_title="Question")
        fig_comp.update_xaxes(tickformat=".0%")
        style_plotly_figure(fig_comp, theme_mode)
        st.plotly_chart(fig_comp, use_container_width=True, key=f"{tab_key}_completion")

    options = [str(q["name"]) for q in questions]
    label_map = {str(q["name"]): str(q.get("label") or q["name"]) for q in questions}

    c1, c2 = st.columns(2)
    question_col = c1.selectbox(
        "Question",
        options,
        format_func=lambda x: label_map.get(x, x),
        key=f"{tab_key}_question",
    )
    breakdown_col = c2.selectbox(
        "Breakdown (optional)",
        ["None"] + [x for x in options if x != question_col],
        key=f"{tab_key}_breakdown",
    )

    selected_question = next((q for q in questions if str(q.get("name", "")) == question_col), questions[0])
    _render_single_question(
        data=org_data,
        question=selected_question,
        breakdown_col=breakdown_col,
        template=template,
        theme_mode=theme_mode,
        key=tab_key,
    )

    with st.expander("Section data preview", expanded=False):
        preview_cols = options[: min(10, len(options))]
        st.dataframe(_safe_preview(org_data, preview_cols, limit=300), use_container_width=True, hide_index=True)

