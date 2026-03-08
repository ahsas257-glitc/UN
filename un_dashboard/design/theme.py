"""Liquid Glass Ultra theme and shared presentation helpers."""

from __future__ import annotations

from html import escape
from typing import Literal, Sequence

import streamlit as st

ThemeMode = Literal["light", "dark"]


def configure_page() -> None:
    st.set_page_config(
        page_title="UN Women Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def resolve_theme_mode() -> ThemeMode:
    try:
        locked = str(st.secrets.get("LOCKED_THEME_MODE", "")).strip().lower()
    except Exception:
        locked = ""
    if locked in {"dark", "light"}:
        return "dark" if locked == "dark" else "light"

    try:
        base = str(st.get_option("theme.base") or "").strip().lower()
    except Exception:
        base = ""
    return "dark" if base == "dark" else "light"


def plotly_template_for(mode: ThemeMode) -> str:
    return "plotly_dark" if mode == "dark" else "plotly_white"


def chart_palette_for(mode: ThemeMode) -> list[str]:
    if mode == "dark":
        return ["#77E0FF", "#78F0C8", "#FFCA7A", "#FF92B2", "#8FA6FF", "#D5D2FF"]
    return ["#006A96", "#007D67", "#B65B00", "#BC225E", "#4968D8", "#7457D8"]


def chart_scale_for(mode: ThemeMode) -> list[list[float | str]]:
    if mode == "dark":
        return [
            [0.0, "#08111E"],
            [0.25, "#14304A"],
            [0.5, "#1E597A"],
            [0.75, "#3B93B5"],
            [1.0, "#C9F3FF"],
        ]
    return [
        [0.0, "#F4F9FD"],
        [0.25, "#D3E6F2"],
        [0.5, "#95C0D6"],
        [0.75, "#4C8AB2"],
        [1.0, "#0E496B"],
    ]


def style_plotly_figure(fig, mode: ThemeMode):
    palette = chart_palette_for(mode)
    scale = chart_scale_for(mode)
    if mode == "dark":
        text_color = "#F8FAFF"
        grid = "rgba(255,255,255,0.08)"
        paper = "rgba(0,0,0,0)"
        plot = "rgba(255,255,255,0.02)"
        hover = "rgba(7,12,22,0.96)"
        line = "rgba(255,255,255,0.18)"
    else:
        text_color = "#17324A"
        grid = "rgba(23,50,74,0.08)"
        paper = "rgba(255,255,255,0)"
        plot = "rgba(255,255,255,0.18)"
        hover = "rgba(255,255,255,0.98)"
        line = "rgba(23,50,74,0.12)"

    fig.update_layout(
        paper_bgcolor=paper,
        plot_bgcolor=plot,
        font=dict(color=text_color, size=12, family="'Aptos', 'Segoe UI', 'Inter', sans-serif"),
        colorway=palette,
        hovermode="x unified",
        hoverlabel=dict(bgcolor=hover, bordercolor=line, font=dict(color=text_color, size=11)),
        legend=dict(
            orientation="h",
            y=1.05,
            x=0,
            yanchor="bottom",
            xanchor="left",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color=text_color),
        ),
        margin=dict(l=32, r=22, t=68, b=32),
        coloraxis=dict(colorscale=scale),
    )
    fig.update_xaxes(
        automargin=True,
        showline=True,
        linecolor=grid,
        gridcolor=grid,
        zerolinecolor=grid,
        tickfont=dict(color=text_color, size=11),
        title_font=dict(color=text_color, size=12),
    )
    fig.update_yaxes(
        automargin=True,
        showline=True,
        linecolor=grid,
        gridcolor=grid,
        zerolinecolor=grid,
        tickfont=dict(color=text_color, size=11),
        title_font=dict(color=text_color, size=12),
    )
    fig.update_traces(marker_line_width=0.9, marker_line_color=line, selector={"type": "bar"})
    fig.update_traces(line={"width": 2.4}, marker={"line": {"width": 0.9, "color": line}}, selector={"type": "scatter"})
    fig.update_traces(marker={"line": {"width": 0.9, "color": line}}, selector={"type": "pie"})
    fig.update_traces(opacity=0.96, selector={"type": "heatmap"})
    return fig


def inject_liquid_glass_theme(mode: ThemeMode) -> None:
    if mode == "dark":
        palette = {
            "bg": "#020617",
            "bg_2": "#07111F",
            "surface": "rgba(12, 20, 33, 0.68)",
            "surface_alt": "rgba(14, 28, 45, 0.78)",
            "surface_soft": "rgba(255,255,255,0.06)",
            "border": "rgba(255,255,255,0.14)",
            "border_strong": "rgba(255,255,255,0.24)",
            "text": "#F8FBFF",
            "muted": "#B8C8D9",
            "accent": "#57D4FF",
            "accent_2": "#65F0C4",
            "accent_3": "#A78BFA",
            "shadow": "0 20px 50px rgba(0,0,0,0.35)",
        }
    else:
        palette = {
            "bg": "#F2F8FC",
            "bg_2": "#EAF1F7",
            "surface": "rgba(255, 255, 255, 0.62)",
            "surface_alt": "rgba(255, 255, 255, 0.82)",
            "surface_soft": "rgba(255,255,255,0.32)",
            "border": "rgba(19, 50, 78, 0.10)",
            "border_strong": "rgba(19, 50, 78, 0.18)",
            "text": "#17324A",
            "muted": "#607286",
            "accent": "#1A82BA",
            "accent_2": "#00A87E",
            "accent_3": "#6B5CE7",
            "shadow": "0 20px 48px rgba(19, 50, 78, 0.10)",
        }

    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {{
    --bg: {palette['bg']};
    --bg-2: {palette['bg_2']};
    --surface: {palette['surface']};
    --surface-alt: {palette['surface_alt']};
    --surface-soft: {palette['surface_soft']};
    --border: {palette['border']};
    --border-strong: {palette['border_strong']};
    --text: {palette['text']};
    --muted: {palette['muted']};
    --accent: {palette['accent']};
    --accent-2: {palette['accent_2']};
    --accent-3: {palette['accent_3']};
    --shadow: {palette['shadow']};
}}

html, body, .stApp {{
    font-family: 'Manrope', 'Segoe UI', sans-serif !important;
    color: var(--text) !important;
    background:
        radial-gradient(circle at 15% 20%, rgba(87,212,255,0.16), transparent 28%),
        radial-gradient(circle at 84% 18%, rgba(103,240,196,0.14), transparent 26%),
        radial-gradient(circle at 72% 78%, rgba(167,139,250,0.14), transparent 28%),
        linear-gradient(180deg, var(--bg), var(--bg-2)) !important;
}}

#MainMenu,
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
    display: none !important;
}}

.stApp::before,
.stApp::after {{
    content: "";
    position: fixed;
    inset: auto;
    width: 26rem;
    height: 26rem;
    border-radius: 50%;
    filter: blur(70px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.48;
}}

.stApp::before {{
    top: 1rem;
    left: -5rem;
    background: rgba(87, 212, 255, 0.18);
    animation: floatA 15s ease-in-out infinite;
}}

.stApp::after {{
    right: -5rem;
    bottom: 1rem;
    background: rgba(103, 240, 196, 0.14);
    animation: floatB 18s ease-in-out infinite;
}}

@keyframes floatA {{
    0%, 100% {{ transform: translate3d(0,0,0) scale(1); }}
    50% {{ transform: translate3d(2rem, 1rem, 0) scale(1.08); }}
}}

@keyframes floatB {{
    0%, 100% {{ transform: translate3d(0,0,0) scale(1); }}
    50% {{ transform: translate3d(-1.5rem, -1rem, 0) scale(1.1); }}
}}

.main .block-container {{
    max-width: 1480px;
    padding: 1rem 1.35rem 1.8rem !important;
    position: relative;
    z-index: 1;
}}

[data-testid="stSidebar"] > div {{
    background: linear-gradient(180deg, var(--surface-alt), var(--surface)) !important;
    border-right: 1px solid var(--border);
    backdrop-filter: blur(28px) saturate(160%);
}}

[data-testid="stMetric"],
[data-testid="stDataFrame"],
[data-testid="stTable"],
[data-testid="stPlotlyChart"],
.streamlit-expanderHeader,
[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-baseweb="textarea"] {{
    background: linear-gradient(180deg, var(--surface-alt), var(--surface)) !important;
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(28px) saturate(165%);
    -webkit-backdrop-filter: blur(28px) saturate(165%);
    box-shadow: var(--shadow);
}}

[data-testid="stMetric"] {{
    border-radius: 22px;
    padding: 1rem 1rem;
    position: relative;
    overflow: hidden;
}}

[data-testid="stMetric"]::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, transparent 15%, rgba(255,255,255,0.14) 48%, transparent 78%);
    transform: translateX(-120%);
    animation: shimmer 7s linear infinite;
}}

@keyframes shimmer {{
    0% {{ transform: translateX(-120%); }}
    35% {{ transform: translateX(120%); }}
    100% {{ transform: translateX(120%); }}
}}

div[data-testid="stMetricValue"] > div {{
    font-size: 2.08rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}}

div[data-testid="stMetricLabel"] > div {{
    color: var(--muted) !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
}}

.stButton > button,
.stDownloadButton > button {{
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3)) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 16px 34px rgba(27, 118, 164, 0.18) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 18px 42px rgba(27, 118, 164, 0.26) !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 0.35rem;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 999px;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
}}

[data-baseweb="radio"] > div {{
    gap: 0.45rem;
    display: flex;
    flex-wrap: wrap;
}}

[data-baseweb="radio"] label {{
    background: linear-gradient(180deg, var(--surface-alt), var(--surface));
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.48rem 0.95rem;
    cursor: pointer;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}}

[data-baseweb="radio"] label:hover {{
    transform: translateY(-1px);
    border-color: var(--border-strong);
    box-shadow: 0 14px 26px rgba(18, 64, 101, 0.12);
}}

[data-baseweb="radio"] label:has(input:checked) {{
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3)) !important;
    border-color: transparent !important;
    box-shadow: 0 16px 32px rgba(18, 102, 142, 0.22);
}}

[data-baseweb="radio"] label:has(input:checked) span,
[data-baseweb="radio"] label:has(input:checked) div,
[data-baseweb="radio"] label:has(input:checked) p {{
    color: #FFFFFF !important;
    font-weight: 800 !important;
}}

.ultra-hero {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(140deg, rgba(255,255,255,0.16), rgba(255,255,255,0.03));
    border: 1px solid var(--border-strong);
    border-radius: 28px;
    padding: 1.35rem 1.45rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    backdrop-filter: blur(30px) saturate(170%);
}}

.ultra-hero::before {{
    content: "";
    position: absolute;
    inset: -30%;
    background: radial-gradient(circle at 25% 25%, rgba(87,212,255,0.22), transparent 26%),
                radial-gradient(circle at 82% 30%, rgba(167,139,250,0.20), transparent 24%),
                radial-gradient(circle at 70% 82%, rgba(103,240,196,0.16), transparent 24%);
    animation: halo 16s linear infinite;
}}

@keyframes halo {{
    0% {{ transform: rotate(0deg) scale(1); }}
    50% {{ transform: rotate(180deg) scale(1.04); }}
    100% {{ transform: rotate(360deg) scale(1); }}
}}

.ultra-hero > * {{
    position: relative;
    z-index: 1;
}}

.ultra-badge-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 0.75rem;
}}

.ultra-badge {{
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.14);
    color: var(--text);
    font-size: 0.8rem;
    font-weight: 700;
}}

.ultra-hero h1 {{
    margin: 0;
    font-size: 2rem;
    line-height: 1.12;
    font-weight: 800;
    color: var(--text);
}}

.ultra-hero p {{
    margin: 0.6rem 0 0;
    max-width: 72rem;
    font-size: 0.98rem;
    color: var(--muted);
    line-height: 1.55;
}}

.ultra-stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.75rem;
    margin: 0.9rem 0 1rem;
}}

.ultra-stat {{
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 0.95rem 1rem;
    background: linear-gradient(180deg, var(--surface-alt), var(--surface));
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    backdrop-filter: blur(24px) saturate(165%);
}}

.ultra-stat::after {{
    content: "";
    position: absolute;
    inset: auto 0 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
}}

.ultra-stat-label {{
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}

.ultra-stat-value {{
    margin-top: 0.35rem;
    color: var(--text);
    font-size: 1.55rem;
    font-weight: 800;
}}

.ultra-stat-note {{
    margin-top: 0.25rem;
    color: var(--muted);
    font-size: 0.84rem;
}}

.ultra-list-card {{
    border-radius: 22px;
    padding: 1rem 1.05rem;
    background: linear-gradient(180deg, var(--surface-alt), var(--surface));
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom: 0.85rem;
}}

.ultra-list-card h3 {{
    margin: 0 0 0.75rem;
    font-size: 1rem;
    font-weight: 800;
    color: var(--text);
}}

.ultra-list-card ul {{
    margin: 0;
    padding-left: 1.1rem;
}}

.ultra-list-card li {{
    color: var(--muted);
    margin-bottom: 0.4rem;
    line-height: 1.5;
}}

.lg-section-title {{
    margin: 0.45rem 0 0.35rem;
    font-size: 1.08rem;
    font-weight: 800;
    color: var(--text);
}}

.lg-section-caption {{
    margin: 0 0 0.85rem;
    color: var(--muted);
    font-size: 0.92rem;
}}

@media (max-width: 768px) {{
    .main .block-container {{
        padding: 0.75rem 0.7rem 1.2rem !important;
    }}

    .ultra-hero h1 {{
        font-size: 1.45rem;
    }}
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


def render_hero() -> None:
    render_report_hero(
        title="UN Women Monitoring Dashboard",
        subtitle="Advanced monitoring, reporting, time intelligence, and export workflows in a liquid-glass interface.",
        badges=["Monitoring", "Reporting", "Visualizing"],
    )


def section_heading(title: str, caption: str = "") -> None:
    st.markdown(f"<div class='lg-section-title'>{escape(title)}</div>", unsafe_allow_html=True)
    if caption:
        st.markdown(f"<div class='lg-section-caption'>{escape(caption)}</div>", unsafe_allow_html=True)


def render_report_hero(title: str, subtitle: str, badges: Sequence[str] | None = None) -> None:
    badge_html = ""
    if badges:
        badge_html = "<div class='ultra-badge-row'>" + "".join(
            f"<span class='ultra-badge'>{escape(str(item))}</span>" for item in badges if str(item).strip()
        ) + "</div>"
    st.markdown(
        f"""
<div class="ultra-hero">
    {badge_html}
    <h1>{escape(title)}</h1>
    <p>{escape(subtitle)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def clickable_tabs(
    options: Sequence[str],
    *,
    key: str,
    label: str = "Navigation",
    index: int = 0,
) -> str:
    choices = [str(option) for option in options if str(option).strip()]
    if not choices:
        return ""
    safe_index = min(max(index, 0), len(choices) - 1)
    return st.radio(
        label,
        choices,
        index=safe_index,
        horizontal=True,
        key=key,
        label_visibility="collapsed",
    )


def render_glass_stats(items: Sequence[dict[str, str]]) -> None:
    cards = []
    for item in items:
        label = escape(str(item.get("label", "")))
        value = escape(str(item.get("value", "")))
        note = escape(str(item.get("note", "")))
        cards.append(
            f"""
<div class="ultra-stat">
    <div class="ultra-stat-label">{label}</div>
    <div class="ultra-stat-value">{value}</div>
    <div class="ultra-stat-note">{note}</div>
</div>
"""
        )
    st.markdown(f"<div class='ultra-stats'>{''.join(cards)}</div>", unsafe_allow_html=True)


def render_glass_list(title: str, items: Sequence[str]) -> None:
    entries = "".join(f"<li>{escape(str(item))}</li>" for item in items if str(item).strip())
    if not entries:
        entries = "<li>No items available.</li>"
    st.markdown(
        f"""
<div class="ultra-list-card">
    <h3>{escape(title)}</h3>
    <ul>{entries}</ul>
</div>
""",
        unsafe_allow_html=True,
    )
