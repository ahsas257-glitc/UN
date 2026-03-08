"""Organization-level dashboard/report/updater/pivot/builder views."""

from __future__ import annotations

import io
import uuid

import pandas as pd
import plotly.express as px
import streamlit as st

from un_dashboard.core.constants import (
    CORRECTION_LOG_SHEET,
    DEFAULT_XLS_FORMS_DIR,
    ORG_SHEET_TABS,
    TARGET_INTERVIEWS_PER_ORG,
)
from un_dashboard.design import (
    ThemeMode,
    clickable_tabs,
    render_glass_list,
    render_glass_stats,
    render_report_hero,
    section_heading,
    style_plotly_figure,
)
from un_dashboard.questionnaires import get_questionnaire_for_sheet_name
from un_dashboard.services.sheets import (
    append_worksheet_rows,
    get_worksheet_header,
    list_worksheet_titles,
    load_worksheet_df,
    parse_sheet_id,
    update_worksheet_header,
)
from un_dashboard.services.reporting import build_report_artifacts
from un_dashboard.services.transforms import (
    build_daily_interviews,
    find_column,
    format_percent,
    infer_org_code_from_sheet,
    sanitize_for_display,
)
from un_dashboard.views.adaptive_dashboard import render_adaptive_dashboard
from un_dashboard.views.dashboard_router import render_dashboard_by_questionnaire
from un_dashboard.views.gwo_dashboard import render_gwo_dashboard

COUNT_OPTION = "Count (Rows)"
AGG_OPTIONS = [COUNT_OPTION, "Sum", "Mean", "Median", "Min", "Max", "Distinct Count"]
AGG_MAP = {
    "Sum": "sum",
    "Mean": "mean",
    "Median": "median",
    "Min": "min",
    "Max": "max",
    "Distinct Count": "nunique",
}


def _safe_read_excel_sheet(file_bytes: bytes, sheet_name: str) -> pd.DataFrame:
    try:
        return pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet_name, engine="openpyxl")
    except Exception:
        return pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet_name)


def _normalize_df_for_sheets(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]

    # Use positional access so duplicate labels never break datetime normalization.
    for idx, dtype in enumerate(out.dtypes):
        if str(dtype).startswith("datetime64"):
            dt_series = pd.to_datetime(out.iloc[:, idx], errors="coerce")
            out.iloc[:, idx] = dt_series.dt.strftime("%Y-%m-%d %H:%M:%S")

    out = out.astype(object).where(pd.notnull(out), "")

    def _fix_cell(x):
        if hasattr(x, "to_pydatetime"):
            try:
                return x.to_pydatetime().strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return str(x)
        if hasattr(x, "isoformat") and not isinstance(x, str):
            try:
                return x.isoformat(sep=" ")
            except Exception:
                return str(x)
        return x

    return out.applymap(_fix_cell)


def _ensure_uuid_in_dest_header(dest_header: list[str], uuid_col: str = "_uuid") -> tuple[list[str], bool]:
    cleaned = [str(h).strip() for h in dest_header if str(h).strip() != ""]
    if uuid_col in cleaned:
        return cleaned, False
    return cleaned + [uuid_col], True


def _build_aligned_df(
    upload_df: pd.DataFrame,
    dest_header: list[str],
) -> tuple[pd.DataFrame, list[str], list[str]]:
    frame = upload_df.copy()
    frame.columns = [str(c).strip() for c in frame.columns]

    dest_header = [str(h).strip() for h in dest_header]
    dest_set = set(dest_header)
    upload_set = set(frame.columns)

    unmatched_dest = [h for h in dest_header if h not in upload_set]
    unused_upload = [c for c in frame.columns if c not in dest_set]

    aligned = pd.DataFrame(index=frame.index)
    for h in dest_header:
        if h in frame.columns:
            aligned[h] = frame[h]
        else:
            aligned[h] = ""

    return aligned, unmatched_dest, unused_upload


def _generate_missing_uuids(series: pd.Series) -> tuple[pd.Series, int]:
    s = series.astype(str).fillna("").map(lambda x: x.strip())
    missing_mask = (s == "") | (s.str.lower() == "nan")
    generated = int(missing_mask.sum())
    if generated:
        s.loc[missing_mask] = [str(uuid.uuid4()) for _ in range(generated)]
    return s, generated


def _existing_uuid_set_from_sheet_df(dest_df: pd.DataFrame, uuid_col: str = "_uuid") -> set[str]:
    if dest_df is None or dest_df.empty or uuid_col not in dest_df.columns:
        return set()
    s = dest_df[uuid_col].astype(str).fillna("").map(lambda x: x.strip())
    return {x for x in s.tolist() if x}


def _rows_from_df(df: pd.DataFrame) -> list[list[object]]:
    return df.values.tolist()


def _default_destination_index(options: list[str], selected_org: str) -> int:
    if not options:
        return 0
    if selected_org in options:
        return options.index(selected_org)
    preferred_exact = f"{selected_org}-Beneficiaries"
    if preferred_exact in options:
        return options.index(preferred_exact)

    selected_org_upper = selected_org.upper()
    for idx, name in enumerate(options):
        if selected_org_upper in str(name).upper():
            return idx
    return 0


def _project_choices(data: pd.DataFrame) -> list[str]:
    base = ORG_SHEET_TABS.copy()
    if data.empty or "sheet_name" not in data.columns:
        return base

    available = {str(x).strip() for x in data["sheet_name"].dropna().astype(str).tolist() if str(x).strip()}
    extras = sorted([name for name in available if name not in set(base)], key=str.lower)
    return base + extras


def _preferred_start_column(org_data: pd.DataFrame, indicators: dict[str, str | None]) -> str | None:
    start_col = find_column(org_data, ["start"])
    if start_col and start_col in org_data.columns:
        return start_col

    date_col = indicators.get("date")
    if date_col and date_col in org_data.columns:
        return date_col

    fallback = find_column(org_data, ["date_time", "submissiondate", "interview_date", "today"])
    if fallback and fallback in org_data.columns:
        return fallback
    return None


def _render_start_timeline_panel(
    org_data: pd.DataFrame,
    indicators: dict[str, str | None],
    template: str,
    theme_mode: ThemeMode,
) -> None:
    section_heading("Start-Date Timeline", "Daily interview count and cumulative progress from the interview start field.")

    date_col = _preferred_start_column(org_data, indicators)
    if not date_col:
        st.info("No start/date column was detected for timeline rendering.")
        return

    trend = build_daily_interviews(org_data, date_col)
    if trend.empty:
        st.info(f"Column `{date_col}` is present, but no valid dates were found for timeline rendering.")
        return

    peak_row = trend.sort_values("interviews", ascending=False).iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Active days", f"{len(trend):,}")
    c2.metric("Peak daily interviews", f"{int(peak_row['interviews']):,}")
    c3.metric("Latest cumulative", f"{int(trend['cumulative'].iloc[-1]):,}")

    fig = px.bar(
        trend,
        x="date",
        y="interviews",
        color="interviews",
        template=template,
        title=f"Daily Interviews by `{date_col}`",
    )
    fig.add_scatter(
        x=trend["date"],
        y=trend["cumulative"],
        mode="lines+markers",
        name="Cumulative",
        yaxis="y2",
    )
    fig.update_layout(
        yaxis_title="Daily interviews",
        xaxis_title="Date",
        yaxis2=dict(title="Cumulative", overlaying="y", side="right"),
        legend=dict(orientation="h"),
    )
    style_plotly_figure(fig, theme_mode)
    st.plotly_chart(fig, use_container_width=True)


def _canonical_first_tabs(source_tabs: list[str]) -> list[str]:
    canonical = [name for name in ORG_SHEET_TABS if str(name).strip().lower() != CORRECTION_LOG_SHEET.lower()]
    canonical_lookup = {name.lower() for name in canonical}

    cleaned_source: list[str] = []
    seen: set[str] = set()
    for raw in source_tabs:
        name = str(raw).strip()
        key = name.lower()
        if not name or key == CORRECTION_LOG_SHEET.lower() or key in seen:
            continue
        seen.add(key)
        cleaned_source.append(name)

    if not cleaned_source:
        return canonical

    source_lookup = {name.lower() for name in cleaned_source}
    ordered = [name for name in canonical if name.lower() in source_lookup]
    extras = sorted([name for name in cleaned_source if name.lower() not in canonical_lookup], key=str.lower)
    return ordered + extras


def _render_dataset_updater_tab(
    all_data: pd.DataFrame,
    selected_org: str,
    sheet_url: str,
    service_info: dict | None,
) -> None:
    section_heading("Updater", "Import Excel rows, align by destination header, and append to Google Sheet.")

    if not service_info:
        st.warning("Google service account is required for updater append workflow.")
        return

    try:
        sheet_id = parse_sheet_id(sheet_url)
    except Exception as exc:
        st.error(f"Invalid Google Sheet URL: {exc}")
        return

    worksheet_options: list[str] = []
    remote_tabs: list[str] = []
    try:
        remote_tabs = list_worksheet_titles(sheet_id, service_info)
    except Exception as exc:
        st.warning(f"Could not read worksheet names from Google Sheet: {exc}")
    worksheet_options = _canonical_first_tabs(remote_tabs)

    if not remote_tabs and "sheet_name" in all_data.columns:
        data_tabs = all_data["sheet_name"].dropna().astype(str).unique().tolist()
        worksheet_options = _canonical_first_tabs(data_tabs)

    if not worksheet_options:
        st.error("No destination worksheet options found.")
        return

    updater_key = f"updater_{selected_org}"
    tool = st.selectbox(
        "Destination Google Sheet tab",
        worksheet_options,
        index=_default_destination_index(worksheet_options, selected_org),
        key=f"{updater_key}_tool",
    )

    col_a, col_b = st.columns(2)
    require_uuid = col_a.checkbox("Require _uuid (skip row if missing)", value=True, key=f"{updater_key}_require_uuid")
    dedupe_uuid = col_b.checkbox("Skip duplicate _uuid (dedupe)", value=True, key=f"{updater_key}_dedupe_uuid")

    file = st.file_uploader(
        "Upload Excel file (.xlsx)",
        type=["xlsx"],
        accept_multiple_files=False,
        key=f"{updater_key}_file",
    )
    if not file:
        st.info("Upload an .xlsx file to continue.")
        return

    file_bytes = file.getvalue()
    try:
        excel_file = pd.ExcelFile(io.BytesIO(file_bytes), engine="openpyxl")
        excel_sheet_names = excel_file.sheet_names
    except Exception as exc:
        st.error(f"Could not read Excel file: {exc}")
        return

    excel_sheet = st.selectbox(
        "Excel sheet to import",
        excel_sheet_names,
        index=0,
        key=f"{updater_key}_excel_sheet",
    )

    try:
        dest_header_raw = get_worksheet_header(sheet_id, tool, service_info)
    except Exception as exc:
        st.error(f"Could not read destination header: {exc}")
        return

    if not dest_header_raw:
        st.error("Destination header is empty. Ensure the destination tab has a header row.")
        return

    dest_header, header_added_uuid = _ensure_uuid_in_dest_header(dest_header_raw, uuid_col="_uuid")

    try:
        upload_df = _safe_read_excel_sheet(file_bytes, excel_sheet)
    except Exception as exc:
        st.error(f"Could not read selected Excel sheet: {exc}")
        return

    if upload_df is None or upload_df.empty:
        st.warning("Uploaded sheet has no rows.")
        return

    upload_df = _normalize_df_for_sheets(upload_df)
    aligned_df, unmatched_dest_labels, unused_upload_labels = _build_aligned_df(upload_df, dest_header)

    generated_uuid_count = 0
    if "_uuid" in aligned_df.columns:
        aligned_df["_uuid"], generated_uuid_count = _generate_missing_uuids(aligned_df["_uuid"])
    else:
        aligned_df["_uuid"] = ""
        aligned_df["_uuid"], generated_uuid_count = _generate_missing_uuids(aligned_df["_uuid"])

    existing_uuids: set[str] = set()
    skipped_existing_uuid_count = 0
    if dedupe_uuid:
        try:
            dest_df = load_worksheet_df(sheet_id, tool, service_info)
            existing_uuids = _existing_uuid_set_from_sheet_df(dest_df, uuid_col="_uuid")
        except Exception:
            existing_uuids = set()

    uuid_series = aligned_df["_uuid"].astype(str).fillna("").map(lambda x: x.strip())
    require_mask = uuid_series != "" if require_uuid else pd.Series([True] * len(aligned_df), index=aligned_df.index)
    dup_mask = uuid_series.isin(existing_uuids) if (dedupe_uuid and existing_uuids) else pd.Series([False] * len(aligned_df), index=aligned_df.index)

    final_mask = require_mask & (~dup_mask)
    skipped_missing_uuid_count = int((~require_mask).sum())
    skipped_existing_uuid_count = int(dup_mask.sum())
    final_df = aligned_df.loc[final_mask].copy()

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Upload rows", f"{len(upload_df):,}")
    m2.metric("Aligned rows", f"{len(aligned_df):,}")
    m3.metric("Ready to append", f"{len(final_df):,}")
    m4.metric("UUIDs generated", f"{generated_uuid_count:,}")
    m5.metric("Skipped dup UUID", f"{skipped_existing_uuid_count:,}")

    if require_uuid:
        st.caption(f"Skipped missing _uuid: {skipped_missing_uuid_count:,}")

    if unmatched_dest_labels:
        lines = "\n".join([f"- {x}" for x in unmatched_dest_labels[:40]])
        suffix = "\n..." if len(unmatched_dest_labels) > 40 else ""
        st.warning(
            "These destination columns are not in uploaded Excel and will be appended as empty values:\n\n"
            + lines
            + suffix
        )

    if unused_upload_labels:
        lines = "\n".join([f"- {x}" for x in unused_upload_labels[:40]])
        suffix = "\n..." if len(unused_upload_labels) > 40 else ""
        st.info(
            "These Excel columns are not in destination header and will be ignored:\n\n"
            + lines
            + suffix
        )

    st.markdown("##### Aligned preview (first 200 rows)")
    st.dataframe(aligned_df.head(200), use_container_width=True, hide_index=True)

    append_disabled = len(final_df) == 0
    if st.button("Append rows to Google Sheet", type="primary", disabled=append_disabled, key=f"{updater_key}_append"):
        try:
            if header_added_uuid:
                update_worksheet_header(sheet_id, tool, dest_header, service_info)

            rows_to_append = _rows_from_df(final_df[dest_header])
            append_worksheet_rows(sheet_id, tool, rows_to_append, service_info)
            st.success(f"Appended {len(rows_to_append):,} rows to '{tool}'.")
            st.cache_data.clear()
            st.rerun()
        except Exception as exc:
            st.error(f"Append failed: {exc}")


def _to_numeric(series: pd.Series) -> pd.Series:
    clean = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(clean, errors="coerce")


def _numeric_like_columns(df: pd.DataFrame, threshold: float = 0.70) -> list[str]:
    numeric_cols: list[str] = []
    for col in df.columns:
        series = df[col]
        if pd.api.types.is_numeric_dtype(series):
            numeric_cols.append(col)
            continue

        sample = series.dropna().astype(str).head(400)
        if sample.empty:
            continue
        ratio = _to_numeric(sample).notna().mean()
        if ratio >= threshold:
            numeric_cols.append(col)
    return numeric_cols


def _safe_unique_values(series: pd.Series, limit: int = 300) -> list[str]:
    values = (
        series.dropna()
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .unique()
        .tolist()
    )
    values = sorted(values)
    return values[:limit]


def _flatten_pivot_table(pivot_df: pd.DataFrame) -> pd.DataFrame:
    display = pivot_df.copy()
    if isinstance(display.columns, pd.MultiIndex):
        display.columns = [
            " | ".join([str(part) for part in col if str(part) != ""])
            for col in display.columns.to_flat_index()
        ]
    else:
        display.columns = [str(col) for col in display.columns]
    return display.reset_index()


def _aggregate_for_chart(
    df: pd.DataFrame,
    dimensions: list[str],
    metric_col: str | None,
    agg_label: str,
) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[*dimensions, "metric"])

    if agg_label == COUNT_OPTION:
        if dimensions:
            return df.groupby(dimensions, dropna=False).size().reset_index(name="metric")
        return pd.DataFrame({"metric": [len(df)]})

    if not metric_col or metric_col not in df.columns:
        return pd.DataFrame(columns=[*dimensions, "metric"])

    if agg_label == "Distinct Count":
        if dimensions:
            return (
                df.groupby(dimensions, dropna=False)[metric_col]
                .nunique(dropna=True)
                .reset_index(name="metric")
            )
        return pd.DataFrame({"metric": [df[metric_col].nunique(dropna=True)]})

    work = df.copy()
    work["__metric__"] = _to_numeric(work[metric_col])
    work = work.dropna(subset=["__metric__"])
    if work.empty:
        return pd.DataFrame(columns=[*dimensions, "metric"])

    agg_func = AGG_MAP.get(agg_label, "sum")
    if dimensions:
        return (
            work.groupby(dimensions, dropna=False)["__metric__"]
            .agg(agg_func)
            .reset_index(name="metric")
        )
    return pd.DataFrame({"metric": [getattr(work["__metric__"], agg_func)()]})


def _render_pivot_tables_tab(org_data: pd.DataFrame, selected_org: str) -> None:
    section_heading("Pivot Tables", "Build accurate pivot summaries for the selected organization.")
    if org_data.empty:
        st.info("No data found for this organization.")
        return

    key = f"pivot_{selected_org}"
    cols = org_data.columns.tolist()
    numeric_like = _numeric_like_columns(org_data)

    c1, c2, c3 = st.columns(3)
    row_fields = c1.multiselect("Rows", cols, key=f"{key}_rows")
    col_candidates = [c for c in cols if c not in row_fields]
    column_fields = c2.multiselect("Columns", col_candidates, key=f"{key}_cols")
    agg_label = c3.selectbox("Aggregation", AGG_OPTIONS, index=0, key=f"{key}_agg")

    filter_col = st.selectbox("Quick filter column (optional)", ["None"] + cols, key=f"{key}_filter_col")
    filtered = org_data.copy()
    if filter_col != "None":
        filter_values = _safe_unique_values(org_data[filter_col], limit=300)
        selected_values = st.multiselect(
            "Filter values",
            filter_values,
            key=f"{key}_filter_values",
        )
        if selected_values:
            filtered = filtered[filtered[filter_col].astype(str).isin(selected_values)].copy()

    value_candidates = [c for c in cols if c not in row_fields + column_fields]
    default_value = next((c for c in value_candidates if c in numeric_like), None)
    default_values = [default_value] if default_value and agg_label != COUNT_OPTION else []
    value_fields = st.multiselect(
        "Values",
        value_candidates,
        default=default_values,
        key=f"{key}_values",
    )

    c4, c5, c6 = st.columns(3)
    fill_empty = c4.checkbox("Fill empty with 0", value=True, key=f"{key}_fill")
    show_totals = c5.checkbox("Show totals", value=True, key=f"{key}_totals")
    preview_rows = c6.slider("Preview rows", 20, 2000, 400, 20, key=f"{key}_preview_rows")

    if not row_fields and not column_fields:
        st.info("Select at least one field in Rows or Columns.")
        return
    if filtered.empty:
        st.info("No rows left after applying filters.")
        return
    if agg_label != COUNT_OPTION and not value_fields:
        st.warning("For this aggregation, please choose one or more value columns.")
        return

    work = filtered.copy()
    fill_value = 0 if fill_empty else None
    try:
        if agg_label == COUNT_OPTION:
            work["__records__"] = 1
            pivot_df = pd.pivot_table(
                work,
                index=row_fields or None,
                columns=column_fields or None,
                values="__records__",
                aggfunc="sum",
                fill_value=fill_value,
                margins=show_totals,
                margins_name="Total",
                observed=False,
            )
        else:
            for value_col in value_fields:
                if value_col in numeric_like:
                    work[value_col] = _to_numeric(work[value_col])
            pivot_df = pd.pivot_table(
                work,
                index=row_fields or None,
                columns=column_fields or None,
                values=value_fields,
                aggfunc=AGG_MAP[agg_label],
                fill_value=fill_value,
                margins=show_totals,
                margins_name="Total",
                observed=False,
            )
    except Exception as exc:
        st.error(f"Pivot table could not be built: {exc}")
        return

    if pivot_df is None or pivot_df.empty:
        st.info("Pivot result is empty for the selected configuration.")
        return

    display_df = _flatten_pivot_table(pivot_df)
    st.caption(f"Rows used: {len(filtered):,} | Pivot rows shown: {min(len(display_df), preview_rows):,}")
    st.dataframe(display_df.head(preview_rows), use_container_width=True, hide_index=True)
    st.download_button(
        "Download Pivot CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected_org}_pivot_table.csv",
        mime="text/csv",
        key=f"{key}_download",
    )


def _render_custom_chart_tab(
    org_data: pd.DataFrame,
    selected_org: str,
    template: str,
    theme_mode: ThemeMode,
) -> None:
    section_heading("Custom Chart & Analysis", "Create interactive charts instantly from selected columns.")
    if org_data.empty:
        st.info("No data found for this organization.")
        return

    key = f"builder_{selected_org}"
    cols = org_data.columns.tolist()
    numeric_like = _numeric_like_columns(org_data)
    chart_types = [
        "Bar",
        "Grouped Bar",
        "Stacked Bar",
        "Horizontal Bar",
        "Line",
        "Area",
        "Scatter",
        "Bubble",
        "Histogram",
        "Box",
        "Violin",
        "Pie",
        "Donut",
        "Heatmap",
        "Treemap",
        "Sunburst",
        "Funnel",
    ]

    top1, top2, top3 = st.columns(3)
    chart_type = top1.selectbox("Chart type", chart_types, key=f"{key}_chart_type")
    agg_label = top2.selectbox("Aggregation", AGG_OPTIONS, index=0, key=f"{key}_agg")
    max_rows = top3.slider("Max rows for plotting", 500, 50000, 8000, 500, key=f"{key}_max_rows")

    filter_col = st.selectbox("Quick filter column (optional)", ["None"] + cols, key=f"{key}_filter_col")
    filtered = org_data.copy()
    if filter_col != "None":
        filter_values = _safe_unique_values(org_data[filter_col], limit=300)
        selected_values = st.multiselect("Filter values", filter_values, key=f"{key}_filter_values")
        if selected_values:
            filtered = filtered[filtered[filter_col].astype(str).isin(selected_values)].copy()

    if filtered.empty:
        st.info("No rows left after applying filters.")
        return

    plot_df = filtered.head(max_rows).copy() if len(filtered) > max_rows else filtered.copy()
    if len(filtered) > max_rows:
        st.caption(f"Preview limited to first {max_rows:,} rows for speed.")

    c1, c2, c3 = st.columns(3)
    x_col = c1.selectbox("X / Category", cols, key=f"{key}_x")
    y_col = c2.selectbox("Y / Value", ["None"] + cols, key=f"{key}_y")
    color_col = c3.selectbox("Color (optional)", ["None"] + cols, key=f"{key}_color")

    color_arg = None if color_col == "None" else color_col
    y_arg = None if y_col == "None" else y_col
    fig = None
    chart_data = pd.DataFrame()

    try:
        if chart_type in {"Bar", "Grouped Bar", "Stacked Bar", "Horizontal Bar", "Line", "Area", "Pie", "Donut", "Funnel"}:
            dims = [x_col]
            if color_arg and chart_type not in {"Pie", "Donut", "Funnel"}:
                dims.append(color_arg)

            if agg_label != COUNT_OPTION and y_arg is None:
                st.warning("For this aggregation, choose Y / Value column.")
                return

            chart_data = _aggregate_for_chart(filtered, dims, y_arg, agg_label)
            if chart_data.empty:
                st.info("No data available for this chart configuration.")
                return

            if chart_type == "Bar":
                fig = px.bar(chart_data, x=x_col, y="metric", color=color_arg, template=template, title="Custom Bar Chart")
            elif chart_type == "Grouped Bar":
                fig = px.bar(
                    chart_data,
                    x=x_col,
                    y="metric",
                    color=color_arg,
                    barmode="group",
                    template=template,
                    title="Custom Grouped Bar Chart",
                )
            elif chart_type == "Stacked Bar":
                fig = px.bar(
                    chart_data,
                    x=x_col,
                    y="metric",
                    color=color_arg,
                    barmode="stack",
                    template=template,
                    title="Custom Stacked Bar Chart",
                )
            elif chart_type == "Horizontal Bar":
                fig = px.bar(
                    chart_data,
                    x="metric",
                    y=x_col,
                    color=color_arg,
                    orientation="h",
                    template=template,
                    title="Custom Horizontal Bar Chart",
                )
            elif chart_type == "Line":
                fig = px.line(chart_data, x=x_col, y="metric", color=color_arg, markers=True, template=template, title="Custom Line Chart")
            elif chart_type == "Area":
                fig = px.area(chart_data, x=x_col, y="metric", color=color_arg, template=template, title="Custom Area Chart")
            elif chart_type == "Pie":
                fig = px.pie(chart_data, names=x_col, values="metric", template=template, title="Custom Pie Chart")
            elif chart_type == "Donut":
                fig = px.pie(chart_data, names=x_col, values="metric", hole=0.55, template=template, title="Custom Donut Chart")
            elif chart_type == "Funnel":
                fig = px.funnel(chart_data, y=x_col, x="metric", template=template, title="Custom Funnel Chart")

        elif chart_type == "Histogram":
            bins = st.slider("Bins", 5, 120, 30, 1, key=f"{key}_bins")
            chart_data = plot_df[[x_col] + ([color_arg] if color_arg else [])].copy()
            fig = px.histogram(
                chart_data,
                x=x_col,
                color=color_arg,
                nbins=bins,
                template=template,
                title="Custom Histogram",
            )

        elif chart_type in {"Scatter", "Bubble", "Box", "Violin"}:
            if y_arg is None:
                st.warning("Please choose Y / Value for this chart type.")
                return

            chart_data = plot_df.copy()
            x_plot = x_col
            y_plot = y_arg
            if x_col in numeric_like:
                chart_data["__x_num__"] = _to_numeric(chart_data[x_col])
                x_plot = "__x_num__"
            if y_arg in numeric_like:
                chart_data["__y_num__"] = _to_numeric(chart_data[y_arg])
                y_plot = "__y_num__"

            if chart_type == "Scatter":
                fig = px.scatter(chart_data, x=x_plot, y=y_plot, color=color_arg, template=template, title="Custom Scatter Chart")
            elif chart_type == "Bubble":
                size_col = st.selectbox(
                    "Bubble size column",
                    ["None"] + numeric_like,
                    key=f"{key}_size",
                )
                size_arg = None if size_col == "None" else size_col
                if size_arg:
                    chart_data["__size_num__"] = _to_numeric(chart_data[size_arg])
                    fig = px.scatter(
                        chart_data,
                        x=x_plot,
                        y=y_plot,
                        size="__size_num__",
                        color=color_arg,
                        template=template,
                        title="Custom Bubble Chart",
                    )
                else:
                    fig = px.scatter(chart_data, x=x_plot, y=y_plot, color=color_arg, template=template, title="Custom Bubble Chart")
            elif chart_type == "Box":
                fig = px.box(chart_data, x=x_col, y=y_plot, color=color_arg, template=template, title="Custom Box Plot")
            elif chart_type == "Violin":
                fig = px.violin(chart_data, x=x_col, y=y_plot, color=color_arg, box=True, template=template, title="Custom Violin Plot")

        elif chart_type == "Heatmap":
            row_col = st.selectbox("Heatmap row field", cols, key=f"{key}_heat_row")
            value_col = st.selectbox("Heatmap value (for non-count)", ["None"] + cols, key=f"{key}_heat_value")

            if agg_label == COUNT_OPTION:
                heat = filtered.groupby([row_col, x_col], dropna=False).size().unstack(fill_value=0)
            else:
                if value_col == "None":
                    st.warning("Select Heatmap value for this aggregation.")
                    return
                work = filtered.copy()
                work["__metric__"] = _to_numeric(work[value_col])
                work = work.dropna(subset=["__metric__"])
                if work.empty:
                    st.info("No numeric values available for heatmap.")
                    return
                heat = (
                    work.groupby([row_col, x_col], dropna=False)["__metric__"]
                    .agg(AGG_MAP[agg_label])
                    .unstack(fill_value=0)
                )

            if heat.empty:
                st.info("No data available for heatmap.")
                return

            if heat.shape[0] > 40 or heat.shape[1] > 40:
                heat = heat.iloc[:40, :40]
                st.caption("Heatmap limited to first 40x40 categories for speed.")

            chart_data = heat.reset_index()
            fig = px.imshow(heat, text_auto=True, aspect="auto", template=template, title="Custom Heatmap")

        elif chart_type in {"Treemap", "Sunburst"}:
            path_cols = st.multiselect(
                "Hierarchy columns",
                cols,
                default=[x_col],
                key=f"{key}_path_cols",
            )
            value_col = st.selectbox("Value column (for non-count)", ["None"] + cols, key=f"{key}_tree_value")
            if not path_cols:
                st.warning("Select at least one hierarchy column.")
                return
            if agg_label != COUNT_OPTION and value_col == "None":
                st.warning("Select a value column for this aggregation.")
                return

            metric_col = None if agg_label == COUNT_OPTION else value_col
            chart_data = _aggregate_for_chart(filtered, path_cols, metric_col, agg_label)
            if chart_data.empty:
                st.info("No data available for hierarchy chart.")
                return

            if chart_type == "Treemap":
                fig = px.treemap(chart_data, path=path_cols, values="metric", color="metric", template=template, title="Custom Treemap")
            else:
                fig = px.sunburst(chart_data, path=path_cols, values="metric", color="metric", template=template, title="Custom Sunburst")

        if fig is None:
            st.info("Select chart fields to render.")
            return

        style_plotly_figure(fig, theme_mode)
        fig.update_layout(transition_duration=0)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]},
        )

        if st.checkbox("Show chart data table", value=False, key=f"{key}_show_data"):
            if chart_data.empty:
                st.info("No table rows to show for current configuration.")
            else:
                st.dataframe(chart_data.head(1500), use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Chart builder error: {exc}")


def render_organization_section(
    data: pd.DataFrame,
    master: pd.DataFrame,
    progress: pd.DataFrame,
    indicators: dict[str, str | None],
    correction_log: pd.DataFrame,
    sheet_url: str,
    openai_key: str,
    openai_model: str,
    service_info: dict | None,
    template: str,
    theme_mode: ThemeMode,
    forms_dir: str = DEFAULT_XLS_FORMS_DIR,
) -> None:
    project_choices = _project_choices(data)
    selected_project = st.selectbox("Select Organization", options=project_choices)
    selected_org_code = infer_org_code_from_sheet(selected_project)

    if "sheet_name" in data.columns:
        org_data = data[data["sheet_name"].astype(str) == selected_project].copy()
    else:
        org_data = data[data["org_code"] == selected_org_code].copy()

    org_progress_row = progress[progress["org_code"] == selected_org_code].head(1)

    active_section = clickable_tabs(
        ["Dashboard", "Report", "Updater", "Pivot Tables", "Chart Builder"],
        key=f"org_module_tabs_{selected_org_code}",
        label="Organization module",
    )

    if active_section == "Dashboard":
        project_questionnaire = get_questionnaire_for_sheet_name(selected_project)
        province = (
            str(org_data["province"].dropna().astype(str).mode().iloc[0])
            if "province" in org_data.columns and not org_data["province"].dropna().empty
            else (org_progress_row["province"].iloc[0] if not org_progress_row.empty else "Unknown")
        )
        partner = (
            str(org_data["ingo_partner"].dropna().astype(str).mode().iloc[0])
            if "ingo_partner" in org_data.columns and not org_data["ingo_partner"].dropna().empty
            else (org_progress_row["ingo_partner"].iloc[0] if not org_progress_row.empty else "Unknown")
        )
        interviews = int(len(org_data))
        progress_pct = (interviews / TARGET_INTERVIEWS_PER_ORG) if TARGET_INTERVIEWS_PER_ORG else 0.0

        with st.container():
            section_heading("Organization Snapshot")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Organization", selected_project)
            col2.metric("Province", province)
            col3.metric("INGO Partner", partner)
            col4.metric("Interviews", f"{interviews}/{TARGET_INTERVIEWS_PER_ORG}")
            st.progress(min(max(progress_pct, 0.0), 1.0))

        _render_start_timeline_panel(
            org_data=org_data,
            indicators=indicators,
            template=template,
            theme_mode=theme_mode,
        )

        if project_questionnaire and project_questionnaire.key == "gwo_beneficiaries":
            gwo_tabs = project_questionnaire.org_dashboard_tabs if project_questionnaire.org_dashboard_tabs else {}
            render_gwo_dashboard(org_data, gwo_tabs, template, theme_mode)
        else:
            rendered = render_dashboard_by_questionnaire(
                org_data=org_data,
                questionnaire=project_questionnaire,
                project_name=selected_project,
                forms_dir=forms_dir,
                template=template,
                theme_mode=theme_mode,
            )
            if not rendered:
                render_adaptive_dashboard(
                    org_data=org_data,
                    project_name=selected_project,
                    forms_dir=forms_dir,
                    template=template,
                    theme_mode=theme_mode,
                    questionnaire=project_questionnaire,
                )

    elif active_section == "Report":
        province = (
            str(org_data["province"].dropna().astype(str).mode().iloc[0])
            if "province" in org_data.columns and not org_data["province"].dropna().empty
            else (org_progress_row["province"].iloc[0] if not org_progress_row.empty else "Unknown")
        )
        partner = (
            str(org_data["ingo_partner"].dropna().astype(str).mode().iloc[0])
            if "ingo_partner" in org_data.columns and not org_data["ingo_partner"].dropna().empty
            else (org_progress_row["ingo_partner"].iloc[0] if not org_progress_row.empty else "Unknown")
        )
        interviews = int(len(org_data))
        progress_pct = (interviews / TARGET_INTERVIEWS_PER_ORG) if TARGET_INTERVIEWS_PER_ORG else 0.0

        with st.container():
            section_heading("Organization Report Center", "Full PDF, Word, and Excel report for the selected organization with narrative insights and charts.")
            if org_data.empty:
                st.info("No data found for this organization.")
            else:
                report_scope = f"{selected_project} ({selected_org_code})"
                artifacts = build_report_artifacts(
                    scope_kind="organization",
                    scope_label=report_scope,
                    data=org_data,
                    progress=org_progress_row,
                    indicators=indicators,
                    theme_mode=theme_mode,
                )

                metric_map = {row["Metric"]: row["Value"] for _, row in artifacts["summary_table"].iterrows()}
                render_report_hero(
                    title=f"{selected_project} Advanced Report",
                    subtitle="Premium organization report with KPI intelligence, narrative analysis, and a modern start-date interview timeline.",
                    badges=[selected_org_code, province, partner, "PDF", "Word", "Excel"],
                )
                render_glass_stats(
                    [
                        {"label": "Interviews", "value": metric_map.get("Interviews analyzed", "0"), "note": "Records in this organization"},
                        {"label": "Completion", "value": metric_map.get("Completion", "N/A"), "note": "Against organization target"},
                        {"label": "Projects", "value": metric_map.get("Projects covered", "0"), "note": "Sheet scope represented"},
                        {"label": "Completeness", "value": metric_map.get("Data completeness", "N/A"), "note": "Key-indicator coverage"},
                    ]
                )

                info_col, risk_col, rec_col = st.columns(3)
                with info_col:
                    render_glass_list("Executive Summary", artifacts["insights"])
                with risk_col:
                    render_glass_list("Key Risks", artifacts["risks"])
                with rec_col:
                    render_glass_list("Recommendations", artifacts["recommendations"])

                st.write(f"- Organization: **{selected_project}**")
                st.write(f"- Organization Code: **{selected_org_code}**")
                st.write(f"- Province: **{province}**")
                st.write(f"- INGO Partner: **{partner}**")
                st.write(f"- Interviews: **{interviews}/{TARGET_INTERVIEWS_PER_ORG}**")
                st.write(f"- Completion: **{format_percent(progress_pct)}**")

                metric_map = {row["Metric"]: row["Value"] for _, row in artifacts["summary_table"].iterrows()}
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Interviews", metric_map.get("Interviews analyzed", "0"))
                m2.metric("Completion", metric_map.get("Completion", "—"))
                m3.metric("Projects", metric_map.get("Projects covered", "0"))
                m4.metric("Data completeness", metric_map.get("Data completeness", "—"))

                st.markdown("##### Executive Summary")
                for item in artifacts["insights"]:
                    st.write(f"- {item}")

                st.markdown("##### Key Risks")
                for item in artifacts["risks"]:
                    st.write(f"- {item}")

                st.markdown("##### Recommendations")
                for item in artifacts["recommendations"]:
                    st.write(f"- {item}")

                st.dataframe(artifacts["indicator_table"], use_container_width=True, hide_index=True)

                section_heading("Core Analytical Visuals", "High-value visuals included in the downloadable organization report.")
                for chart in artifacts["charts"]:
                    st.markdown(f"##### {chart['title']}")
                    st.caption(chart["caption"])
                    st.image(chart["image"], use_container_width=True)
                    st.dataframe(chart["table"].head(20), use_container_width=True, hide_index=True)

                org_activity_sections = artifacts.get("org_activity_sections", [])
                if org_activity_sections:
                    section_heading(
                        "Start-Date Interview Timeline",
                        "Exact daily interview count for this organization based on the `start` field, including weekday pattern.",
                    )
                    activity_section = org_activity_sections[0]
                    st.markdown(f"##### {activity_section['title']}")
                    st.caption(activity_section["caption"])
                    st.image(activity_section["image"], use_container_width=True)
                    st.dataframe(activity_section["table"].head(31), use_container_width=True, hide_index=True)

                safe_preview = sanitize_for_display(org_data).head(300)
                st.markdown("##### Dataset Preview")
                st.dataframe(safe_preview, use_container_width=True, hide_index=True)

                download_cols = st.columns(4)
                download_cols[0].download_button(
                    "Download PDF",
                    data=artifacts["pdf_bytes"],
                    file_name=f"{artifacts['file_stub']}.pdf",
                    mime="application/pdf",
                )
                download_cols[1].download_button(
                    "Download Word",
                    data=artifacts["word_bytes"],
                    file_name=f"{artifacts['file_stub']}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
                download_cols[2].download_button(
                    "Download Excel",
                    data=artifacts["excel_bytes"],
                    file_name=f"{artifacts['file_stub']}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                download_cols[3].download_button(
                    "Download CSV Preview",
                    data=safe_preview.to_csv(index=False).encode("utf-8"),
                    file_name=f"{selected_project}_report.csv",
                    mime="text/csv",
                )

    elif active_section == "Updater":
        _render_dataset_updater_tab(data, selected_project, sheet_url, service_info)

    elif active_section == "Pivot Tables":
        _render_pivot_tables_tab(org_data, selected_project)

    else:
        _render_custom_chart_tab(org_data, selected_project, template, theme_mode)
