"""Liquid Glass iOS 26 Design System for Streamlit UI - Apple's Most Advanced"""

from __future__ import annotations

from typing import Literal

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
    """Use locked admin theme settings (secret/config), not end-user UI toggles."""
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
        return ["#6AD4FF", "#B66CFF", "#63E6C0", "#FFB36B", "#FF82A8", "#6C8CFF"]
    return ["#0066B3", "#8944AB", "#00856A", "#B44C00", "#B32E5E", "#0039B3"]


def chart_scale_for(mode: ThemeMode) -> list[list[float | str]]:
    if mode == "dark":
        return [
            [0.0, "#0A1420"],
            [0.3, "#1E405A"],
            [0.6, "#2F6F8F"],
            [0.8, "#5DB2E6"],
            [1.0, "#A6E0FF"],
        ]
    return [
        [0.0, "#F0F7FF"],
        [0.3, "#B8D6F0"],
        [0.6, "#6FA3D0"],
        [0.8, "#2C699E"],
        [1.0, "#0A3B5E"],
    ]


def style_plotly_figure(fig, mode: ThemeMode):
    palette = chart_palette_for(mode)
    scale = chart_scale_for(mode)
    raw_title = ""
    try:
        raw_title = str(getattr(getattr(fig.layout, "title", None), "text", "") or "").strip()
    except Exception:
        raw_title = ""
    title_text = "" if raw_title.lower() == "undefined" else raw_title
    has_title = bool(title_text)
    top_margin = 118 if has_title else 92
    legend_y = 1.14 if has_title else 1.10

    if mode == "dark":
        layout = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(12,15,20,0.3)",
            font=dict(
                color="#FFFFFF",
                size=13,
                family="'SF Pro Display', 'SF Pro Text', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
            ),
            colorway=palette,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="rgba(22,24,28,0.95)",
                bordercolor="rgba(255,255,255,0.25)",
                font=dict(color="#FFFFFF", size=12, family="'SF Pro Display'"),
            ),
            legend=dict(
                orientation="h",
                y=legend_y,
                x=0,
                yanchor="bottom",
                xanchor="left",
                bgcolor="rgba(20,22,26,0.6)",
                bordercolor="rgba(255,255,255,0.18)",
                borderwidth=1,
                font=dict(size=11, color="#FFFFFF"),
            ),
            margin=dict(l=70, r=50, t=top_margin, b=70, pad=15),
            coloraxis=dict(
                colorscale=scale,
                colorbar=dict(
                    thickness=14,
                    bgcolor="rgba(0,0,0,0)",
                    outlinecolor="rgba(255,255,255,0.25)",
                    tickfont=dict(color="#FFFFFF", size=11),
                    ticks="outside",
                    ticklen=5,
                ),
            ),
        )
        axis_cfg = dict(
            gridcolor="rgba(255,255,255,0.08)",
            zerolinecolor="rgba(255,255,255,0.12)",
            linecolor="rgba(255,255,255,0.15)",
            tickfont=dict(color="#FFFFFF", size=11),
            title_font=dict(color="#FFFFFF", size=12),
        )
        title_color = "#FFFFFF"
        trace_line = "rgba(255,255,255,0.25)"
    else:
        layout = dict(
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(245,247,250,0.5)",
            font=dict(
                color="#1D1D1F",
                size=13,
                family="'SF Pro Display', 'SF Pro Text', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
            ),
            colorway=palette,
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="rgba(255,255,255,0.98)",
                bordercolor="rgba(0,0,0,0.15)",
                font=dict(color="#1D1D1F", size=12, family="'SF Pro Display'"),
            ),
            legend=dict(
                orientation="h",
                y=legend_y,
                x=0,
                yanchor="bottom",
                xanchor="left",
                bgcolor="rgba(255,255,255,0.7)",
                bordercolor="rgba(0,0,0,0.12)",
                borderwidth=1,
                font=dict(size=11, color="#1D1D1F"),
            ),
            margin=dict(l=70, r=50, t=top_margin, b=70, pad=15),
            coloraxis=dict(
                colorscale=scale,
                colorbar=dict(
                    thickness=14,
                    bgcolor="rgba(255,255,255,0)",
                    outlinecolor="rgba(0,0,0,0.15)",
                    tickfont=dict(color="#1D1D1F", size=11),
                    ticks="outside",
                    ticklen=5,
                ),
            ),
        )
        axis_cfg = dict(
            gridcolor="rgba(0,0,0,0.06)",
            zerolinecolor="rgba(0,0,0,0.1)",
            linecolor="rgba(0,0,0,0.15)",
            tickfont=dict(color="#1D1D1F", size=11),
            title_font=dict(color="#1D1D1F", size=12),
        )
        title_color = "#1D1D1F"
        trace_line = "rgba(0,0,0,0.15)"

    fig.update_layout(**layout)
    if has_title:
        fig.update_layout(
            title=dict(
                text=title_text,
                x=0.02,
                y=0.99,
                xanchor="left",
                yanchor="top",
                pad=dict(b=12),
                font=dict(size=16, color=title_color, family="'SF Pro Display', 'Inter', sans-serif"),
            )
        )
    else:
        fig.update_layout(title=None)
    fig.update_xaxes(
        automargin=True,
        title_standoff=15,
        showline=True,
        mirror=False,
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        **axis_cfg,
    )
    fig.update_yaxes(
        automargin=True,
        title_standoff=15,
        showline=True,
        mirror=False,
        ticks="outside",
        ticklen=6,
        tickwidth=1,
        **axis_cfg,
    )
    fig.update_traces(marker_line_width=1.2, marker_line_color=trace_line, selector={"type": "bar"})
    fig.update_traces(line={"width": 2.5}, marker={"line": {"width": 1.2, "color": trace_line}}, selector={"type": "scatter"})
    fig.update_traces(marker={"line": {"color": trace_line, "width": 1.2}}, selector={"type": "pie"})
    fig.update_traces(opacity=0.95, selector={"type": "heatmap"})
    fig.update_traces(opacity=0.95, selector={"type": "histogram"})
    return fig


def inject_liquid_glass_theme(mode: ThemeMode) -> None:
    if mode == "dark":
        palette = {
            "bg_primary": "#000000",
            "bg_secondary": "#0A0A0C",
            "bg_tertiary": "#141416",
            "text_primary": "#FFFFFF",
            "text_secondary": "#EBEBF5",
            "text_tertiary": "#C6C6C8",
            "text_muted": "#8E8E93",
            "glass_ultra_thin": "rgba(255, 255, 255, 0.04)",
            "glass_thin": "rgba(255, 255, 255, 0.08)",
            "glass_regular": "rgba(255, 255, 255, 0.12)",
            "glass_thick": "rgba(255, 255, 255, 0.16)",
            "glass_ultra_thick": "rgba(255, 255, 255, 0.2)",
            "border_thin": "rgba(255, 255, 255, 0.1)",
            "border_regular": "rgba(255, 255, 255, 0.2)",
            "border_thick": "rgba(255, 255, 255, 0.3)",
            "shadow_small": "0 8px 20px rgba(0, 0, 0, 0.4)",
            "shadow_medium": "0 16px 32px rgba(0, 0, 0, 0.5)",
            "shadow_large": "0 24px 48px rgba(0, 0, 0, 0.6)",
            "shadow_glow": "0 0 30px rgba(10, 132, 255, 0.3)",
            "accent_blue": "#0A84FF",
            "accent_purple": "#BF5AF2",
            "accent_pink": "#FF375F",
            "accent_green": "#32D74B",
            "accent_orange": "#FF9F0A",
            "accent_teal": "#64D2FF",
            "gradient_primary": "linear-gradient(135deg, #0A84FF, #BF5AF2)",
            "gradient_secondary": "linear-gradient(135deg, #FF375F, #FF9F0A)",
            "orb_blue": "rgba(10, 132, 255, 0.2)",
            "orb_purple": "rgba(191, 90, 242, 0.18)",
            "orb_pink": "rgba(255, 55, 95, 0.16)",
            "table_head": "rgba(255, 255, 255, 0.08)",
            "input_bg": "rgba(255, 255, 255, 0.07)",
            "surface": "rgba(18, 18, 20, 0.7)",
            "success": "#30D158",
            "warning": "#FF9F0A",
            "error": "#FF453A",
            "info": "#64D2FF",
        }
    else:
        palette = {
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F5F5F7",
            "bg_tertiary": "#FAFAFC",
            "text_primary": "#1D1D1F",
            "text_secondary": "#3A3A3C",
            "text_tertiary": "#6B6B70",
            "text_muted": "#8E8E93",
            "glass_ultra_thin": "rgba(255, 255, 255, 0.3)",
            "glass_thin": "rgba(255, 255, 255, 0.5)",
            "glass_regular": "rgba(255, 255, 255, 0.7)",
            "glass_thick": "rgba(255, 255, 255, 0.85)",
            "glass_ultra_thick": "rgba(255, 255, 255, 0.95)",
            "border_thin": "rgba(0, 0, 0, 0.08)",
            "border_regular": "rgba(0, 0, 0, 0.15)",
            "border_thick": "rgba(0, 0, 0, 0.25)",
            "shadow_small": "0 8px 20px rgba(0, 0, 0, 0.06)",
            "shadow_medium": "0 16px 32px rgba(0, 0, 0, 0.1)",
            "shadow_large": "0 24px 48px rgba(0, 0, 0, 0.15)",
            "shadow_glow": "0 0 30px rgba(0, 122, 255, 0.2)",
            "accent_blue": "#007AFF",
            "accent_purple": "#5856D6",
            "accent_pink": "#FF2D55",
            "accent_green": "#34C759",
            "accent_orange": "#FF9500",
            "accent_teal": "#5AC8FA",
            "gradient_primary": "linear-gradient(135deg, #007AFF, #5856D6)",
            "gradient_secondary": "linear-gradient(135deg, #FF2D55, #FF9500)",
            "orb_blue": "rgba(0, 122, 255, 0.1)",
            "orb_purple": "rgba(88, 86, 214, 0.08)",
            "orb_pink": "rgba(255, 45, 85, 0.06)",
            "table_head": "rgba(0, 0, 0, 0.04)",
            "input_bg": "rgba(255, 255, 255, 0.9)",
            "surface": "rgba(255, 255, 255, 0.8)",
            "success": "#28CD41",
            "warning": "#FF9500",
            "error": "#FF3B30",
            "info": "#5AC8FA",
        }

    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ============================================
   ROOT VARIABLES - iOS 26 INSPIRED
   ============================================ */
:root {{
    --bg-primary: {palette['bg_primary']};
    --bg-secondary: {palette['bg_secondary']};
    --bg-tertiary: {palette['bg_tertiary']};
    --text-primary: {palette['text_primary']};
    --text-secondary: {palette['text_secondary']};
    --text-tertiary: {palette['text_tertiary']};
    --text-muted: {palette['text_muted']};
    
    --glass-ultra-thin: {palette['glass_ultra_thin']};
    --glass-thin: {palette['glass_thin']};
    --glass-regular: {palette['glass_regular']};
    --glass-thick: {palette['glass_thick']};
    --glass-ultra-thick: {palette['glass_ultra_thick']};
    
    --border-thin: {palette['border_thin']};
    --border-regular: {palette['border_regular']};
    --border-thick: {palette['border_thick']};
    
    --shadow-small: {palette['shadow_small']};
    --shadow-medium: {palette['shadow_medium']};
    --shadow-large: {palette['shadow_large']};
    --shadow-glow: {palette['shadow_glow']};
    
    --accent-blue: {palette['accent_blue']};
    --accent-purple: {palette['accent_purple']};
    --accent-pink: {palette['accent_pink']};
    --accent-green: {palette['accent_green']};
    --accent-orange: {palette['accent_orange']};
    --accent-teal: {palette['accent_teal']};
    
    --gradient-primary: {palette['gradient_primary']};
    --gradient-secondary: {palette['gradient_secondary']};
    
    --orb-blue: {palette['orb_blue']};
    --orb-purple: {palette['orb_purple']};
    --orb-pink: {palette['orb_pink']};
    
    --table-head: {palette['table_head']};
    --input-bg: {palette['input_bg']};
    --surface: {palette['surface']};
    
    --success: {palette['success']};
    --warning: {palette['warning']};
    --error: {palette['error']};
    --info: {palette['info']};
}}

/* ============================================
   BASE STYLES
   ============================================ */
html, body, .stApp {{
    background: var(--bg-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
    transition: background 0.3s ease, color 0.2s ease;
}}

.stApp {{
    position: relative;
    min-height: 100vh;
    overflow-x: clip;
}}

/* Lock Streamlit UI controls so end-users cannot change runtime theme */
#MainMenu,
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
    display: none !important;
    visibility: hidden !important;
}}

/* ============================================
   QUANTUM PARTICLE FIELD
   ============================================ */
.quantum-field {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}}

.quantum-particle {{
    position: absolute;
    width: 2px;
    height: 2px;
    background: var(--accent-blue);
    border-radius: 50%;
    opacity: 0;
    filter: blur(1px);
    animation: quantumFloat 15s infinite linear;
}}

@keyframes quantumFloat {{
    0% {{
        transform: translateY(100vh) translateX(0) scale(1);
        opacity: 0;
    }}
    10% {{
        opacity: 0.6;
    }}
    50% {{
        transform: translateY(50vh) translateX(50px) scale(1.5);
        opacity: 0.8;
    }}
    90% {{
        opacity: 0.6;
    }}
    100% {{
        transform: translateY(-100px) translateX(100px) scale(0.5);
        opacity: 0;
    }}
}}

/* Generate 30 quantum particles */
{''.join([f'''
.quantum-particle:nth-child({i}) {{
    left: {i * 3.3}%;
    animation-delay: {i * 0.2}s;
    background: {['var(--accent-blue)', 'var(--accent-purple)', 'var(--accent-pink)'][i % 3]};
    width: {2 + (i % 3)}px;
    height: {2 + (i % 3)}px;
}}''' for i in range(1, 31)])}

/* ============================================
   3D LIQUID ORBS
   ============================================ */
.liquid-orb {{
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
    pointer-events: none;
    mix-blend-mode: {'screen' if mode == 'dark' else 'multiply'};
    animation: liquidMorph 20s infinite alternate ease-in-out;
}}

.liquid-orb-1 {{
    left: -150px;
    top: -100px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle at 30% 30%, var(--orb-blue), transparent 70%);
    animation-delay: -2s;
}}

.liquid-orb-2 {{
    right: -150px;
    bottom: -100px;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle at 70% 70%, var(--orb-purple), transparent 70%);
    animation-delay: -5s;
}}

.liquid-orb-3 {{
    left: 40%;
    top: 30%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle at 50% 50%, var(--orb-pink), transparent 70%);
    animation-delay: -8s;
}}

@keyframes liquidMorph {{
    0% {{
        transform: translate3d(0, 0, 0) scale(1) rotate(0deg);
        filter: blur(80px);
    }}
    25% {{
        transform: translate3d(50px, -30px, 20px) scale(1.1) rotate(5deg);
        filter: blur(85px);
    }}
    50% {{
        transform: translate3d(-40px, 40px, -20px) scale(0.95) rotate(-5deg);
        filter: blur(75px);
    }}
    75% {{
        transform: translate3d(30px, 30px, 30px) scale(1.05) rotate(3deg);
        filter: blur(82px);
    }}
    100% {{
        transform: translate3d(-20px, -30px, -10px) scale(1) rotate(0deg);
        filter: blur(80px);
    }}
}}

/* ============================================
   MESH GRADIENT BACKGROUND
   ============================================ */
.mesh-gradient {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: {f'radial-gradient(circle at 20% 30%, {palette["orb_blue"]}, transparent 40%), radial-gradient(circle at 80% 70%, {palette["orb_purple"]}, transparent 40%), radial-gradient(circle at 40% 60%, {palette["orb_pink"]}, transparent 40%)'};
    z-index: 0;
    pointer-events: none;
    opacity: 0.8;
}}

/* ============================================
   MAIN CONTAINER
   ============================================ */
.main .block-container {{
    position: relative;
    z-index: 10;
    padding: 1.5rem 2rem !important;
    max-width: 1440px;
    margin: 0 auto;
    animation: fadeInScale 0.8s cubic-bezier(0.2, 0.9, 0.4, 1);
}}

@keyframes fadeInScale {{
    from {{
        opacity: 0;
        transform: scale(0.98) translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: scale(1) translateY(0);
    }}
}}

/* ============================================
   SIDEBAR - LIQUID GLASS
   ============================================ */
[data-testid="stSidebar"] > div {{
    background: var(--surface) !important;
    backdrop-filter: blur(40px) saturate(200%);
    -webkit-backdrop-filter: blur(40px) saturate(200%);
    border-right: 1px solid var(--border-regular);
    box-shadow: var(--shadow-medium);
    transition: all 0.4s cubic-bezier(0.2, 0.9, 0.4, 1);
}}

[data-testid="stSidebar"] > div:hover {{
    box-shadow: var(--shadow-large), var(--shadow-glow);
    border-right-color: var(--border-thick);
}}

[data-testid="stSidebar"] * {{
    color: var(--text-primary) !important;
}}

/* ============================================
   HERO SECTION - IOS 26 LIQUID GLASS
   ============================================ */
.glass-hero {{
    position: relative;
    overflow: hidden;
    background: var(--glass-thick);
    backdrop-filter: blur(50px) saturate(220%);
    -webkit-backdrop-filter: blur(50px) saturate(220%);
    border: 1px solid var(--border-regular);
    border-radius: 40px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-large), inset 0 1px 2px rgba(255,255,255,0.3);
    transform: translateZ(0);
    animation: heroRise 0.8s cubic-bezier(0.2, 0.9, 0.4, 1);
}}

.glass-hero::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.3), transparent 70%);
    opacity: {0.3 if mode == 'dark' else 0.5};
    pointer-events: none;
}}

.glass-hero::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(112deg, 
        transparent 20%, 
        rgba(255,255,255,{0.2 if mode == 'dark' else 0.5}) 45%, 
        transparent 70%
    );
    transform: translateX(-100%);
    animation: heroShimmer 8s infinite;
    pointer-events: none;
}}

@keyframes heroRise {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes heroShimmer {{
    0% {{ transform: translateX(-100%); }}
    20% {{ transform: translateX(100%); }}
    100% {{ transform: translateX(100%); }}
}}

.glass-badge {{
    display: inline-block;
    margin-bottom: 1rem;
    padding: 0.4rem 1.2rem;
    background: var(--glass-ultra-thick);
    border: 1px solid var(--border-thin);
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: var(--accent-blue);
    text-transform: uppercase;
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow-small);
}}

.glass-hero h1 {{
    margin: 0;
    font-size: 2.8rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

.glass-hero p {{
    margin: 1rem 0 0;
    font-size: 1.2rem;
    font-weight: 400;
    color: var(--text-secondary);
    max-width: 700px;
}}

/* ============================================
   METRIC CARDS - 3D LIQUID INTERACTION
   ============================================ */
[data-testid="stMetric"] {{
    position: relative;
    background: var(--glass-regular);
    backdrop-filter: blur(40px) saturate(200%);
    -webkit-backdrop-filter: blur(40px) saturate(200%);
    border: 1px solid var(--border-thin);
    border-radius: 28px;
    padding: 1.5rem 1.8rem;
    box-shadow: var(--shadow-medium), inset 0 1px 2px rgba(255,255,255,0.2);
    transition: all 0.4s cubic-bezier(0.2, 0.9, 0.4, 1);
    overflow: hidden;
    cursor: pointer;
}}

[data-testid="stMetric"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
                rgba(255,255,255,{0.3 if mode == 'dark' else 0.4}), 
                transparent 70%);
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-6px) scale(1.02);
    box-shadow: var(--shadow-large), var(--shadow-glow), inset 0 1px 3px rgba(255,255,255,0.3);
    border-color: var(--border-regular);
}}

[data-testid="stMetric"]:hover::before {{
    opacity: 0.4;
}}

div[data-testid="stMetricValue"] > div {{
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    background: var(--gradient-primary);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 0.3rem !important;
}}

div[data-testid="stMetricLabel"] > div {{
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

div[data-testid="stMetricDelta"] > div {{
    font-size: 0.9rem !important;
    color: var(--success) !important;
}}

/* ============================================
   TABS - NEOMORPHIC GLASS
   ============================================ */
.stTabs [data-baseweb="tab-list"] {{
    background: var(--glass-regular);
    backdrop-filter: blur(30px) saturate(180%);
    -webkit-backdrop-filter: blur(30px) saturate(180%);
    border: 1px solid var(--border-thin);
    border-radius: 100px;
    padding: 0.5rem;
    gap: 0.5rem;
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.2), var(--shadow-small);
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 100px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    color: var(--text-secondary) !important;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

.stTabs [data-baseweb="tab"]::before {{
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: var(--gradient-primary);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s ease, height 0.6s ease;
    opacity: 0.1;
}}

.stTabs [data-baseweb="tab"]:hover::before {{
    width: 200px;
    height: 200px;
}}

.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: var(--gradient-primary);
    color: white !important;
    box-shadow: var(--shadow-glow);
}}

/* ============================================
   BUTTONS - LIQUID METAL
   ============================================ */
.stButton > button,
.stDownloadButton > button {{
    border-radius: 16px !important;
    border: 1px solid var(--border-regular) !important;
    background: var(--gradient-primary) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    box-shadow: var(--shadow-medium), inset 0 1px 2px rgba(255,255,255,0.3) !important;
    transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1) !important;
    position: relative;
    overflow: hidden;
}}

.stButton > button::after,
.stDownloadButton > button::after {{
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(112deg, 
                transparent, 
                rgba(255, 255, 255, 0.3), 
                transparent);
    transform: rotate(25deg) translateX(-100%);
    transition: transform 0.6s ease;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: var(--shadow-large), var(--shadow-glow), inset 0 1px 3px rgba(255,255,255,0.4) !important;
}}

.stButton > button:hover::after,
.stDownloadButton > button:hover::after {{
    transform: rotate(25deg) translateX(100%);
}}

/* ============================================
   INPUT FIELDS - DEEP GLASS
   ============================================ */
[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="select"] > div {{
    background: var(--input-bg) !important;
    border: 1px solid var(--border-thin) !important;
    border-radius: 14px !important;
    color: var(--text-primary) !important;
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    transition: all 0.2s ease;
}}

[data-baseweb="input"]:hover,
[data-baseweb="textarea"]:hover,
[data-baseweb="select"] > div:hover {{
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px {palette['accent_blue']}20;
}}

[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within,
[data-baseweb="select"] > div:focus-within {{
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px {palette['accent_blue']}30;
}}

/* ============================================
   DATA FRAME - LIQUID TABLE
   ============================================ */
[data-testid="stDataFrame"],
[data-testid="stTable"] {{
    background: var(--glass-regular);
    border: 1px solid var(--border-thin);
    border-radius: 24px;
    backdrop-filter: blur(30px) saturate(180%);
    -webkit-backdrop-filter: blur(30px) saturate(180%);
    box-shadow: var(--shadow-medium);
    overflow: hidden;
}}

[data-testid="stDataFrame"] [role="columnheader"] {{
    background: var(--table-head) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    padding: 1rem !important;
}}

[data-testid="stDataFrame"] [role="cell"] {{
    color: var(--text-secondary) !important;
    padding: 0.8rem 1rem !important;
    border-bottom: 1px solid var(--border-thin) !important;
}}

/* ============================================
   PROGRESS BAR - LIQUID GRADIENT
   ============================================ */
[data-testid="stProgressBar"] > div > div > div > div {{
    background: var(--gradient-primary) !important;
    border-radius: 100px !important;
    animation: progressPulse 2s infinite;
}}

@keyframes progressPulse {{
    0% {{ opacity: 1; }}
    50% {{ opacity: 0.8; }}
    100% {{ opacity: 1; }}
}}

/* ============================================
   PLOTLY CHARTS - GLASS CONTAINER
   ============================================ */
[data-testid="stPlotlyChart"] {{
    background: var(--glass-regular);
    border: 1px solid var(--border-thin);
    border-radius: 28px;
    padding: 1.2rem;
    backdrop-filter: blur(30px) saturate(180%);
    -webkit-backdrop-filter: blur(30px) saturate(180%);
    box-shadow: var(--shadow-medium);
    transition: all 0.3s ease;
}}

[data-testid="stPlotlyChart"]:hover {{
    box-shadow: var(--shadow-large), var(--shadow-glow);
    border-color: var(--border-regular);
}}

/* ============================================
   EXPANDER - GLASS
   ============================================ */
.streamlit-expanderHeader {{
    background: var(--glass-regular) !important;
    border: 1px solid var(--border-thin) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    color: var(--text-primary) !important;
}}

.streamlit-expanderContent {{
    background: var(--glass-thin) !important;
    border: 1px solid var(--border-thin) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    backdrop-filter: blur(20px) !important;
}}

/* ============================================
   CHECKBOX & RADIO - GLASS
   ============================================ */
.stCheckbox,
.stRadio {{
    background: var(--glass-thin);
    border: 1px solid var(--border-thin);
    border-radius: 16px;
    padding: 1rem;
    backdrop-filter: blur(20px);
}}

/* ============================================
   SECTION HEADINGS
   ============================================ */
.lg-section-title {{
    margin: 0.5rem 0 0.75rem;
    font-size: 1.2rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.01em;
}}

.lg-section-caption {{
    margin: -0.5rem 0 1.5rem;
    color: var(--text-tertiary);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* ============================================
   SCROLLBAR STYLING
   ============================================ */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: var(--glass-thin);
}}

::-webkit-scrollbar-thumb {{
    background: var(--border-regular);
    border-radius: 100px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--accent-blue);
}}

/* ============================================
   FLAT LAYOUT (NO EXTRA CONTAINER / CARD BORDERS)
   ============================================ */
[data-testid="stVerticalBlockBorderWrapper"] {{
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    padding: 0.15rem 0 !important;
}}

[data-testid="stPlotlyChart"],
[data-testid="stDataFrame"],
[data-testid="stTable"] {{
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
}}

[data-testid="stMetric"] {{
    position: relative;
    overflow: hidden;
    border: 1.2px solid var(--accent-blue) !important;
    background: linear-gradient(140deg, var(--glass-thick), var(--glass-regular)) !important;
    backdrop-filter: blur(28px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
    box-shadow: var(--shadow-medium), 0 0 0 1px rgba(255,255,255,0.08) inset !important;
}}

[data-testid="stMetric"]::before {{
    display: block !important;
    opacity: 0.28 !important;
    background: radial-gradient(
        240px circle at var(--mouse-x, 50%) var(--mouse-y, 45%),
        rgba(255,255,255,0.28),
        transparent 65%
    ) !important;
}}

[data-testid="stMetric"]::after {{
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.24);
    pointer-events: none;
}}

[data-testid="stMetric"]:hover,
[data-testid="stPlotlyChart"]:hover {{
    transform: none !important;
}}

[data-testid="stMetric"]:hover {{
    border-color: var(--accent-teal) !important;
    box-shadow: var(--shadow-large), var(--shadow-glow), 0 0 0 1px rgba(255,255,255,0.10) inset !important;
}}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */
@media (max-width: 1200px) {{
    .glass-hero h1 {{
        font-size: 2.2rem;
    }}
}}

@media (max-width: 900px) {{
    .glass-hero {{
        padding: 1.8rem;
    }}
    
    .glass-hero h1 {{
        font-size: 1.8rem;
    }}
    
    .glass-hero p {{
        font-size: 1rem;
    }}
    
    div[data-testid="stMetricValue"] > div {{
        font-size: 2rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.4rem 1.2rem;
        font-size: 0.9rem;
    }}
}}

@media (max-width: 600px) {{
    .main .block-container {{
        padding: 1rem !important;
    }}
    
    .glass-hero {{
        border-radius: 28px;
        padding: 1.2rem;
    }}
    
    .glass-hero h1 {{
        font-size: 1.4rem;
    }}
    
    .glass-badge {{
        font-size: 0.7rem;
        padding: 0.3rem 0.8rem;
    }}
}}
</style>

<!-- Quantum Particle Field -->
<div class="quantum-field">
    {''.join([f'<div class="quantum-particle"></div>' for _ in range(30)])}
</div>

<!-- Liquid Orbs -->
<div class="liquid-orb liquid-orb-1"></div>
<div class="liquid-orb liquid-orb-2"></div>
<div class="liquid-orb liquid-orb-3"></div>

<!-- Mesh Gradient -->
<div class="mesh-gradient"></div>

<!-- Mouse Tracking Script -->
<script>
document.addEventListener('DOMContentLoaded', function() {{
    // Mouse tracking for metric cards
    const metrics = document.querySelectorAll('[data-testid="stMetric"]');
    metrics.forEach(metric => {{
        metric.addEventListener('mousemove', function(e) {{
            const rect = this.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            this.style.setProperty('--mouse-x', x + '%');
            this.style.setProperty('--mouse-y', y + '%');
        }});
    }});
    
    // Add hover effect to buttons
    const buttons = document.querySelectorAll('.stButton > button, .stDownloadButton > button');
    buttons.forEach(button => {{
        button.addEventListener('mouseenter', function() {{
            this.style.transform = 'translateY(-3px) scale(1.02)';
        }});
        button.addEventListener('mouseleave', function() {{
            this.style.transform = 'translateY(0) scale(1)';
        }});
    }});
}});
</script>
"""
    st.markdown(css, unsafe_allow_html=True)


def render_hero() -> None:
    """Render the iOS 26 Liquid Glass hero section"""
    st.markdown(
        """
<div class="glass-hero">
    UN WOMEN - Monitoring Dashboard
</div>
""",
        unsafe_allow_html=True,
    )


def section_heading(title: str, caption: str = "") -> None:
    """Render a section heading with optional caption"""
    st.markdown(f"<div class='lg-section-title'>{title}</div>", unsafe_allow_html=True)
    if caption:
        st.markdown(f"<div class='lg-section-caption'>{caption}</div>", unsafe_allow_html=True)

