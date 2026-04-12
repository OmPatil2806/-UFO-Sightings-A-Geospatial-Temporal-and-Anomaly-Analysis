"""
╔══════════════════════════════════════════════════════════════════╗
║   🛸  Global UFO Sightings Intelligence Dashboard               ║
║   Built with Streamlit · Plotly · Pandas                        ║
║   Run:  streamlit run app.py                                     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UFO Sightings Intelligence",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL THEME
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG   = "#0d0d1a"
CARD_BG   = "#12122a"
ACCENT    = "#e94560"
ACCENT2   = "#f5a623"
ACCENT3   = "#4a90e2"
TEXT_MAIN = "#e0e0f0"
TEXT_DIM  = "#8888aa"
GRID_COL  = "#1e1e3a"

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor=CARD_BG,
    plot_bgcolor=DARK_BG,
    font=dict(family="Inter, sans-serif", color=TEXT_MAIN, size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL),
    yaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL),
    hoverlabel=dict(bgcolor=CARD_BG, font_color=TEXT_MAIN, bordercolor=ACCENT),
)

COLOR_SEQ   = [ACCENT, ACCENT2, ACCENT3, "#7ed321", "#9b59b6",
               "#2ecc71", "#e67e22", "#1abc9c", "#e74c3c", "#3498db"]
SEASON_COLS = {"Spring": "#7ed321", "Summer": ACCENT2,
               "Autumn": ACCENT,    "Winter": ACCENT3}

MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
DAY_LABELS   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* ── Global ── */
  html, body, [class*="css"] {{
      font-family: 'Inter', sans-serif;
      background-color: {DARK_BG};
      color: {TEXT_MAIN};
  }}
  .main .block-container {{ padding-top: 1.5rem; max-width: 1400px; }}

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {{
      background: linear-gradient(180deg, #0a0a1a 0%, #12122a 100%);
      border-right: 1px solid #1e1e3a;
  }}
  section[data-testid="stSidebar"] .block-container {{ padding-top: 1rem; }}

  /* ── Metric cards ── */
  div[data-testid="metric-container"] {{
      background: {CARD_BG};
      border: 1px solid #1e1e3a;
      border-radius: 12px;
      padding: 1rem 1.2rem;
      box-shadow: 0 4px 20px rgba(233,69,96,0.08);
  }}
  div[data-testid="metric-container"] label {{
      color: {TEXT_DIM} !important;
      font-size: 0.75rem !important;
      text-transform: uppercase;
      letter-spacing: 0.08em;
  }}
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {{
      color: {TEXT_MAIN} !important;
      font-size: 1.8rem !important;
      font-weight: 700;
  }}

  /* ── Section headers ── */
  .section-header {{
      font-size: 1.5rem;
      font-weight: 700;
      color: {TEXT_MAIN};
      padding: 0.4rem 0 0.8rem 0;
      border-bottom: 2px solid {ACCENT};
      margin-bottom: 1.2rem;
      display: inline-block;
  }}

  /* ── Insight cards ── */
  .insight-card {{
      background: {CARD_BG};
      border-left: 4px solid {ACCENT};
      border-radius: 0 10px 10px 0;
      padding: 0.9rem 1.2rem;
      margin: 0.5rem 0;
      font-size: 0.92rem;
      line-height: 1.6;
  }}
  .insight-card.blue  {{ border-left-color: {ACCENT3}; }}
  .insight-card.green {{ border-left-color: #7ed321; }}
  .insight-card.gold  {{ border-left-color: {ACCENT2}; }}

  /* ── Badge / pill ── */
  .badge {{
      display: inline-block;
      background: rgba(233,69,96,0.15);
      color: {ACCENT};
      border: 1px solid {ACCENT};
      border-radius: 20px;
      padding: 2px 12px;
      font-size: 0.78rem;
      font-weight: 600;
      margin-right: 6px;
  }}

  /* ── Tabs ── */
  button[data-baseweb="tab"] {{
      background: transparent !important;
      color: {TEXT_DIM} !important;
      border-bottom: 2px solid transparent !important;
      font-size: 0.88rem;
  }}
  button[data-baseweb="tab"][aria-selected="true"] {{
      color: {TEXT_MAIN} !important;
      border-bottom: 2px solid {ACCENT} !important;
  }}

  /* ── Sidebar nav labels ── */
  .nav-label {{
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: {TEXT_DIM};
      margin: 1.2rem 0 0.4rem 0;
      font-weight: 600;
  }}

  /* ── Divider ── */
  .custom-divider {{
      border: none;
      border-top: 1px solid #1e1e3a;
      margin: 1.5rem 0;
  }}

  /* ── Plotly chart container ── */
  .js-plotly-plot {{ border-radius: 12px; overflow: hidden; }}

  /* ── Scrollbar ── */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: {DARK_BG}; }}
  ::-webkit-scrollbar-thumb {{ background: #2a2a4a; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="🛸 Loading UFO intelligence database…")
def load_data() -> pd.DataFrame:
    df = pd.read_csv("ufo_sightings_cleaned.csv", low_memory=False)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["comments"]  = df["comments"].fillna("")
    df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")
    df["log_duration"] = pd.to_numeric(df["log_duration"], errors="coerce")
    return df


def apply_filters(df, year_range, countries, shapes):
    """Apply sidebar filters and return filtered dataframe."""
    mask = (
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    )
    if countries:
        mask &= df["country_label"].isin(countries)
    if shapes:
        mask &= df["shape_cleaned"].isin(shapes)
    return df[mask]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Plotly figure defaults
# ─────────────────────────────────────────────────────────────────────────────
def style_fig(fig, title="", height=420):
    fig.update_layout(**PLOTLY_LAYOUT, title=title,
                      title_font_size=15, height=height)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
def page_overview(df, df_full):
    st.markdown('<div class="section-header">🌍 Global Overview</div>',
                unsafe_allow_html=True)

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🛸 Total Sightings",  f"{len(df):,}")
    c2.metric("📅 Year Range",        f"{int(df['year'].min())} – {int(df['year'].max())}")
    c3.metric("🌍 Top Country",       df["country_label"].mode()[0])
    c4.metric("🔵 Most Common Shape", df["shape_cleaned"].mode()[0].title())
    c5.metric("⏱️ Median Duration",   f"{df['duration_min'].median():.1f} min")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Two columns: yearly trend + shape donut ───────────────────────────
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        yearly = df.groupby("year").size().reset_index(name="count")
        rolling = yearly["count"].rolling(5, center=True).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["count"],
            fill="tozeroy", fillcolor="rgba(233,69,96,0.15)",
            line=dict(color=ACCENT, width=2),
            mode="lines", name="Sightings",
            hovertemplate="<b>%{x}</b><br>Sightings: %{y:,}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=yearly["year"], y=rolling,
            line=dict(color=ACCENT2, width=2.5, dash="dot"),
            mode="lines", name="5yr Avg",
            hovertemplate="5yr avg: %{y:,.0f}<extra></extra>"
        ))
        # Annotations for key events
        for yr, label, color in [
            (1994, "Internet Era", "#7ed321"),
            (2007, "Smartphones", ACCENT3),
            (2012, "Peak Year",   ACCENT),
        ]:
            val = yearly[yearly["year"] == yr]["count"].values
            if len(val):
                fig.add_annotation(
                    x=yr, y=val[0], text=f"📌 {label}",
                    showarrow=True, arrowhead=2, arrowcolor=color,
                    ax=0, ay=-45, font=dict(color=color, size=10)
                )
        style_fig(fig, "📈 UFO Sightings Over Time (1906–2014)", height=380)
        fig.update_layout(showlegend=True,
                          legend=dict(bgcolor="rgba(0,0,0,0)", x=0.01, y=0.99))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        shape_counts = df["shape_cleaned"].value_counts().head(9)
        fig2 = go.Figure(go.Pie(
            labels=[s.title() for s in shape_counts.index],
            values=shape_counts.values,
            hole=0.55,
            marker=dict(colors=COLOR_SEQ, line=dict(color=DARK_BG, width=2)),
            textinfo="percent",
            textposition="outside",
            hovertemplate="<b>%{label}</b><br>%{value:,} sightings (%{percent})<extra></extra>"
        ))
        fig2.add_annotation(
            text=f"<b>{len(df):,}</b><br>Total",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=TEXT_MAIN)
        )
        style_fig(fig2, "🔵 Shape Distribution", height=380)
        fig2.update_layout(showlegend=True,
                           legend=dict(bgcolor="rgba(0,0,0,0)",
                                       font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Country bar + Season ring ─────────────────────────────────────────
    col_a, col_b = st.columns([3, 2], gap="large")

    with col_a:
        country_counts = df["country_label"].value_counts().reset_index()
        country_counts.columns = ["Country", "Count"]
        fig3 = px.bar(
            country_counts.head(6),
            x="Count", y="Country",
            orientation="h",
            color="Count",
            color_continuous_scale=[[0, CARD_BG], [1, ACCENT]],
            text="Count",
        )
        fig3.update_traces(
            texttemplate="%{text:,}", textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x:,} sightings<extra></extra>"
        )
        style_fig(fig3, "🌍 Sightings by Country", height=320)
        fig3.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        season_counts = df["season"].value_counts()
        fig4 = go.Figure(go.Pie(
            labels=season_counts.index,
            values=season_counts.values,
            hole=0.5,
            marker=dict(
                colors=[SEASON_COLS.get(s, ACCENT) for s in season_counts.index],
                line=dict(color=DARK_BG, width=2)
            ),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:,}<extra></extra>"
        ))
        style_fig(fig4, "🌸 Seasonal Distribution", height=320)
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # ── Key insights ──────────────────────────────────────────────────────
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown("#### 💡 Key Findings")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(
            '<div class="insight-card">📈 <b>20× growth</b> in sightings after '
            '1994. The internet made NUFORC reporting accessible globally, '
            'dramatically increasing submission volume.</div>',
            unsafe_allow_html=True)
    with i2:
        st.markdown(
            '<div class="insight-card blue">🌍 <b>87% US-based</b> reports. '
            'English-language NUFORC platform and higher internet penetration '
            'create a strong geographic bias in the data.</div>',
            unsafe_allow_html=True)
    with i3:
        st.markdown(
            '<div class="insight-card green">🌞 <b>Summer dominates</b> with 33% '
            'of all sightings. Warmer weather = more outdoor activity = more '
            'night-sky observers.</div>',
            unsafe_allow_html=True)

    # ── Data preview ──────────────────────────────────────────────────────
    with st.expander("📋 View Filtered Dataset Sample", expanded=False):
        st.dataframe(
            df[["datetime","city","country_label","shape_cleaned",
                "duration_min","year","season","time_of_day"]].head(50),
            use_container_width=True,
            hide_index=True
        )

    # Download button
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered Dataset",
        data=csv_data,
        file_name="ufo_filtered.csv",
        mime="text/csv",
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: TEMPORAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def page_temporal(df):
    st.markdown('<div class="section-header">📅 Temporal Analysis</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📆 Yearly & Decade", "🌙 Hour of Day", "📅 Monthly & Season", "🗓️ Day of Week"])

    # ── Tab 1: Yearly / Decade ────────────────────────────────────────────
    with tab1:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            yearly = df.groupby("year").size().reset_index(name="count")
            fig = px.area(yearly, x="year", y="count",
                          color_discrete_sequence=[ACCENT])
            fig.update_traces(
                fillcolor="rgba(233,69,96,0.18)",
                line=dict(width=2),
                hovertemplate="<b>%{x}</b><br>%{y:,} sightings<extra></extra>"
            )
            style_fig(fig, "📈 Annual Sightings (full history)")
            fig.update_layout(xaxis_title="Year", yaxis_title="Sightings")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            decade = df.groupby("decade").size().reset_index(name="count")
            decade["decade_label"] = decade["decade"].astype(str) + "s"
            fig2 = px.bar(decade, x="decade_label", y="count",
                          color="count",
                          color_continuous_scale=[[0, "#1a1a4a"], [1, ACCENT]],
                          text="count")
            fig2.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>%{y:,} sightings<extra></extra>"
            )
            style_fig(fig2, "📊 Sightings by Decade")
            fig2.update_layout(coloraxis_showscale=False,
                               xaxis_title="Decade", yaxis_title="Sightings")
            st.plotly_chart(fig2, use_container_width=True)

        # Animated bar race by decade
        st.markdown("##### 🎬 Shape Popularity Evolution by Decade")
        decade_shape = (
            df.groupby(["decade", "shape_cleaned"])
            .size()
            .reset_index(name="count")
        )
        top_shapes_list = df["shape_cleaned"].value_counts().head(7).index.tolist()
        decade_shape_top = decade_shape[decade_shape["shape_cleaned"].isin(top_shapes_list)]
        fig3 = px.bar(
            decade_shape_top,
            x="shape_cleaned", y="count",
            animation_frame="decade",
            color="shape_cleaned",
            color_discrete_sequence=COLOR_SEQ,
            range_y=[0, decade_shape_top["count"].max() * 1.15],
            labels={"shape_cleaned": "Shape", "count": "Sightings"},
        )
        style_fig(fig3, "Shape Distribution by Decade (Animated)", height=380)
        fig3.update_layout(
            showlegend=False,
            xaxis_title="Shape",
            yaxis_title="Sightings",
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 2: Hour of Day ────────────────────────────────────────────────
    with tab2:
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            hourly = df.groupby("hour").size().reset_index(name="count")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=hourly["hour"], y=hourly["count"],
                marker=dict(
                    color=hourly["count"],
                    colorscale=[[0, "#1a1a4a"], [0.5, ACCENT3], [1, ACCENT]],
                    showscale=False,
                    line=dict(color=DARK_BG, width=0.5)
                ),
                hovertemplate="<b>%{x}:00h</b><br>%{y:,} sightings<extra></extra>"
            ))
            peak_hr = int(hourly.loc[hourly["count"].idxmax(), "hour"])
            fig.add_vline(x=peak_hr, line_dash="dot",
                          line_color=ACCENT2, annotation_text=f"Peak: {peak_hr}:00",
                          annotation_font_color=ACCENT2)
            style_fig(fig, "⏰ Sightings by Hour of Day", height=380)
            fig.update_layout(xaxis=dict(tickmode="linear", dtick=2,
                                         title="Hour (24h)"),
                              yaxis_title="Sightings")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            tod = df["time_of_day"].value_counts().reset_index()
            tod.columns = ["Time", "Count"]
            tod_order = ["Morning (6–12)", "Afternoon (12–18)",
                         "Evening (18–24)", "Night (0–6)"]
            tod["Time"] = pd.Categorical(tod["Time"], categories=tod_order, ordered=True)
            tod = tod.sort_values("Time")

            fig2 = px.bar_polar(
                tod, r="Count", theta="Time",
                color="Count",
                color_continuous_scale=[[0, "#1a1a4a"], [1, ACCENT]],
                template="plotly_dark",
            )
            fig2.update_layout(
                **{k: v for k, v in PLOTLY_LAYOUT.items()
                   if k not in ["xaxis", "yaxis"]},
                title="🌙 Time of Day Breakdown",
                title_font_size=15,
                height=380,
                coloraxis_showscale=False,
                polar=dict(
                    bgcolor=CARD_BG,
                    radialaxis=dict(gridcolor=GRID_COL, tickfont_size=9),
                    angularaxis=dict(gridcolor=GRID_COL)
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Insight
        night_pct = df[df["hour"].isin(range(20, 24))].shape[0] / len(df) * 100
        st.markdown(
            f'<div class="insight-card gold">🌙 <b>{night_pct:.0f}% of sightings '
            f'occur between 20:00–24:00.</b> Darkness combined with wakefulness '
            f'creates the optimal observation window. The 9 PM peak corresponds '
            f'with people relaxing outdoors after dinner.</div>',
            unsafe_allow_html=True)

    # ── Tab 3: Monthly & Season ───────────────────────────────────────────
    with tab3:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            monthly = df.groupby("month").size().reset_index(name="count")
            monthly["month_name"] = [MONTH_LABELS[m-1] for m in monthly["month"]]

            fig = go.Figure(go.Scatterpolar(
                r=monthly["count"],
                theta=monthly["month_name"],
                fill="toself",
                fillcolor="rgba(233,69,96,0.2)",
                line=dict(color=ACCENT, width=2.5),
                name="Sightings",
                hovertemplate="<b>%{theta}</b><br>%{r:,}<extra></extra>"
            ))
            fig.update_layout(
                **{k: v for k, v in PLOTLY_LAYOUT.items()
                   if k not in ["xaxis", "yaxis"]},
                title="🌙 Monthly Pattern (Polar)",
                title_font_size=15,
                height=400,
                polar=dict(
                    bgcolor=CARD_BG,
                    radialaxis=dict(showticklabels=True, gridcolor=GRID_COL,
                                    tickfont_size=8),
                    angularaxis=dict(gridcolor=GRID_COL)
                ),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            monthly_season = (
                df.groupby(["month", "season"])
                .size()
                .reset_index(name="count")
            )
            monthly_season["month_name"] = [
                MONTH_LABELS[m-1] for m in monthly_season["month"]
            ]
            fig2 = px.bar(
                monthly_season,
                x="month_name", y="count",
                color="season",
                color_discrete_map=SEASON_COLS,
                barmode="stack",
                labels={"month_name": "Month", "count": "Sightings",
                        "season": "Season"},
            )
            fig2.update_traces(
                hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>"
            )
            style_fig(fig2, "📅 Monthly Sightings by Season", height=400)
            fig2.update_layout(
                xaxis_title="Month", yaxis_title="Sightings",
                legend=dict(bgcolor="rgba(0,0,0,0)")
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 4: Day of Week ────────────────────────────────────────────────
    with tab4:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            dow = df.groupby("day_of_week").size().reset_index(name="count")
            dow["day_name"] = [DAY_LABELS[d] for d in dow["day_of_week"]]
            fig = px.bar(
                dow, x="day_name", y="count",
                color="count",
                color_continuous_scale=[[0, "#1a1a4a"], [1, ACCENT]],
                text="count",
                labels={"day_name": "Day", "count": "Sightings"}
            )
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>"
            )
            style_fig(fig, "📅 Sightings by Day of Week")
            fig.update_layout(coloraxis_showscale=False,
                               xaxis_title="", yaxis_title="Sightings")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Hour × Day heatmap
            heatmap_data = (
                df.groupby(["hour", "day_of_week"])
                .size()
                .unstack(fill_value=0)
            )
            heatmap_data.columns = DAY_LABELS

            fig2 = go.Figure(go.Heatmap(
                z=heatmap_data.values,
                x=DAY_LABELS,
                y=list(range(24)),
                colorscale=[[0, DARK_BG], [0.4, "#3a0060"],
                             [0.7, ACCENT],  [1, ACCENT2]],
                hovertemplate="<b>%{x} %{y}:00</b><br>%{z:,} sightings<extra></extra>",
                showscale=True,
                colorbar=dict(tickfont=dict(color=TEXT_MAIN))
            ))
            style_fig(fig2, "🔥 Hour × Day of Week Heatmap")
            fig2.update_layout(yaxis_title="Hour (24h)", xaxis_title="Day")
            st.plotly_chart(fig2, use_container_width=True)

        weekend_pct = df[df["is_weekend"] == 1].shape[0] / len(df) * 100
        st.markdown(
            f'<div class="insight-card blue">📅 <b>{weekend_pct:.0f}% of sightings '
            f'occur on weekends.</b> Saturday evenings are the hottest cell in the '
            f'heatmap — people stay up later outdoors, increasing observation time.</div>',
            unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: GEOSPATIAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def page_geospatial(df):
    st.markdown('<div class="section-header">🌍 Geospatial Analysis</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["🌐 Global Map", "🇺🇸 US Deep Dive", "📊 Regional Stats"])

    # ── Tab 1: Global Scatter Map ─────────────────────────────────────────
    with tab1:
        map_size = st.slider("Sample size for map rendering",
                             1000, min(20000, len(df)), 12000, step=1000)
        color_by = st.selectbox("Colour points by",
                                ["shape_cleaned", "season",
                                 "time_of_day", "country_label"],
                                key="geo_color")

        map_df = df.dropna(subset=["latitude", "longitude"]).sample(
            min(map_size, len(df)), random_state=42)

        fig = px.scatter_geo(
            map_df,
            lat="latitude", lon="longitude",
            color=color_by,
            hover_name="city",
            hover_data={
                "year": True,
                "shape_cleaned": True,
                "duration_min": ":.1f",
                "country_label": True,
                "latitude": False,
                "longitude": False,
            },
            color_discrete_sequence=COLOR_SEQ,
            opacity=0.55,
            projection="natural earth",
            title=f"🌍 Global UFO Sightings Map ({map_size:,} sample)"
        )
        fig.update_traces(marker=dict(size=3.5))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=CARD_BG,
            height=560,
            title_font_size=15,
            font_color=TEXT_MAIN,
            geo=dict(
                bgcolor=DARK_BG,
                landcolor="#1a1a3a",
                oceancolor="#0a0a1a",
                showocean=True,
                coastlinecolor="#3a3a6a",
                countrycolor="#2a2a5a",
                showcoastlines=True,
                showcountries=True,
                lakecolor="#0a0a1a",
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10),
            hoverlabel=dict(bgcolor=CARD_BG, font_color=TEXT_MAIN),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 2: US Deep Dive ───────────────────────────────────────────────
    with tab2:
        us_df = df[df["country"] == "us"].copy()
        st.caption(f"Showing {len(us_df):,} US sightings")

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            us_map_df = us_df.dropna(subset=["latitude", "longitude"]).sample(
                min(10000, len(us_df)), random_state=42)

            fig = px.density_mapbox(
                us_map_df,
                lat="latitude", lon="longitude",
                radius=8,
                zoom=3,
                center=dict(lat=39.5, lon=-98.35),
                mapbox_style="carto-darkmatter",
                color_continuous_scale=[[0, "#0a0a1a"],
                                         [0.3, "#3a0060"],
                                         [0.6, ACCENT],
                                         [1.0, ACCENT2]],
                title="🔥 US Sighting Density Heatmap",
                hover_data={"latitude": False, "longitude": False}
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor=CARD_BG,
                height=480,
                title_font_size=14,
                margin=dict(l=0, r=0, t=50, b=0),
                coloraxis_colorbar=dict(
                    title="Density",
                    tickfont=dict(color=TEXT_MAIN)
                )
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            state_counts = us_df["state"].value_counts().head(15).reset_index()
            state_counts.columns = ["State", "Count"]
            fig2 = px.bar(
                state_counts,
                x="Count", y="State",
                orientation="h",
                color="Count",
                color_continuous_scale=[[0, "#1a1a4a"], [1, ACCENT]],
                text="Count",
                labels={"State": "", "Count": "Sightings"}
            )
            fig2.update_traces(
                texttemplate="%{text:,}", textposition="outside",
                hovertemplate="<b>%{y}</b><br>%{x:,}<extra></extra>"
            )
            style_fig(fig2, "📊 Top 15 US States", height=480)
            fig2.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Choropleth
        state_geo = us_df["state"].str.upper().value_counts().reset_index()
        state_geo.columns = ["State", "Count"]
        fig3 = px.choropleth(
            state_geo,
            locations="State",
            locationmode="USA-states",
            color="Count",
            scope="usa",
            color_continuous_scale=[[0, "#0a0a1a"],
                                     [0.3, "#1a1a5a"],
                                     [0.7, ACCENT3],
                                     [1.0, ACCENT]],
            title="🗺️  UFO Sightings Density — US States"
        )
        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor=CARD_BG,
            height=420,
            title_font_size=15,
            geo=dict(bgcolor=DARK_BG, lakecolor=DARK_BG,
                     landcolor="#1a1a3a", subunitcolor="#2a2a5a"),
            coloraxis_colorbar=dict(tickfont=dict(color=TEXT_MAIN))
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 3: Regional Stats ─────────────────────────────────────────────
    with tab3:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            # Country × Shape treemap
            cs = (df.groupby(["country_label", "shape_cleaned"])
                    .size()
                    .reset_index(name="count"))
            cs = cs[cs["country_label"] != "Unknown"]
            fig = px.treemap(
                cs, path=["country_label", "shape_cleaned"],
                values="count",
                color="count",
                color_continuous_scale=[[0, CARD_BG],
                                         [0.5, "#3a0060"],
                                         [1, ACCENT]],
                title="🌲 Country → Shape Treemap"
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor=CARD_BG,
                height=450,
                title_font_size=14,
                margin=dict(l=10, r=10, t=50, b=10),
            )
            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>%{value:,}<extra></extra>"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Country × Season stacked bar
            c_s = (df[df["country_label"] != "Unknown"]
                     .groupby(["country_label", "season"])
                     .size()
                     .reset_index(name="count"))
            fig2 = px.bar(
                c_s,
                x="country_label", y="count",
                color="season",
                color_discrete_map=SEASON_COLS,
                barmode="stack",
                labels={"country_label": "Country",
                        "count": "Sightings", "season": "Season"},
                title="🌐 Country × Season Breakdown"
            )
            style_fig(fig2, "🌐 Country × Season Breakdown", height=450)
            fig2.update_layout(
                xaxis_title="", yaxis_title="Sightings",
                legend=dict(bgcolor="rgba(0,0,0,0)")
            )
            st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: SHAPE & DURATION ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def page_shape_duration(df):
    st.markdown('<div class="section-header">🛸 Shape & Duration Analysis</div>',
                unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔵 Shape Analysis", "⏱️ Duration Analysis"])

    with tab1:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            shape_counts = df["shape_cleaned"].value_counts().reset_index()
            shape_counts.columns = ["Shape", "Count"]
            shape_counts["Shape"] = shape_counts["Shape"].str.title()
            fig = go.Figure(go.Bar(
                x=shape_counts["Count"],
                y=shape_counts["Shape"],
                orientation="h",
                marker=dict(
                    color=shape_counts["Count"],
                    colorscale=[[0, "#1a1a4a"],
                                 [0.5, ACCENT3],
                                 [1, ACCENT]],
                    showscale=False,
                    line=dict(color=DARK_BG, width=0.5)
                ),
                text=shape_counts["Count"],
                texttemplate="%{text:,}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>%{x:,} sightings<extra></extra>"
            ))
            style_fig(fig, "🔵 UFO Shape Frequency")
            fig.update_layout(
                yaxis=dict(categoryorder="total ascending"),
                xaxis_title="Number of Sightings",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Shape over time (top 5)
            top5 = df["shape_cleaned"].value_counts().head(5).index
            shape_year = (
                df[df["shape_cleaned"].isin(top5)]
                .groupby(["year", "shape_cleaned"])
                .size()
                .reset_index(name="count")
            )
            fig2 = px.line(
                shape_year, x="year", y="count",
                color="shape_cleaned",
                color_discrete_sequence=COLOR_SEQ,
                labels={"shape_cleaned": "Shape",
                        "year": "Year", "count": "Sightings"}
            )
            fig2.update_traces(line_width=2)
            style_fig(fig2, "📈 Top 5 Shape Trends Over Time")
            fig2.update_layout(
                xaxis_title="Year", yaxis_title="Sightings",
                legend=dict(bgcolor="rgba(0,0,0,0)", title="Shape")
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Shape × Hour heatmap
        shape_hour = (
            df.groupby(["shape_cleaned", "hour"])
            .size()
            .unstack(fill_value=0)
        )
        fig3 = go.Figure(go.Heatmap(
            z=shape_hour.values,
            x=list(range(24)),
            y=[s.title() for s in shape_hour.index],
            colorscale=[[0, DARK_BG], [0.4, "#3a0060"],
                         [0.7, ACCENT], [1, ACCENT2]],
            hovertemplate="<b>%{y}</b> at %{x}:00<br>%{z:,} sightings<extra></extra>",
            showscale=True,
            colorbar=dict(tickfont=dict(color=TEXT_MAIN))
        ))
        style_fig(fig3, "🔥 Shape × Hour Heatmap", height=400)
        fig3.update_layout(
            xaxis=dict(title="Hour (24h)", tickmode="linear", dtick=2),
            yaxis_title="Shape"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            dur_df = df.dropna(subset=["duration_min"])
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=dur_df["log_duration"],
                nbinsx=60,
                marker=dict(
                    color=ACCENT,
                    opacity=0.75,
                    line=dict(color=DARK_BG, width=0.5)
                ),
                name="Log Duration",
                hovertemplate="log-duration: %{x:.1f}<br>Count: %{y:,}<extra></extra>"
            ))
            median_log = dur_df["log_duration"].median()
            fig.add_vline(x=median_log, line_dash="dot",
                          line_color=ACCENT2,
                          annotation_text=f"Median: {dur_df['duration_min'].median():.0f} min",
                          annotation_font_color=ACCENT2)
            style_fig(fig, "⏱️ Duration Distribution (Log Scale)")
            fig.update_layout(xaxis_title="log(1 + seconds)",
                              yaxis_title="Frequency", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Duration box by shape
            top6 = df["shape_cleaned"].value_counts().head(6).index
            box_df = df[df["shape_cleaned"].isin(top6)].dropna(subset=["log_duration"])
            fig2 = go.Figure()
            for i, shape in enumerate(top6):
                subset = box_df[box_df["shape_cleaned"] == shape]["log_duration"]
                fig2.add_trace(go.Box(
                    y=subset,
                    name=shape.title(),
                    marker_color=COLOR_SEQ[i % len(COLOR_SEQ)],
                    boxmean=True,
                    hovertemplate=f"<b>{shape.title()}</b><br>%{{y:.2f}}<extra></extra>"
                ))
            style_fig(fig2, "📦 Duration by Shape (Log Scale)")
            fig2.update_layout(
                yaxis_title="log(1 + seconds)",
                xaxis_title="Shape",
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Duration by hour scatter
        dur_hour = (
            df.dropna(subset=["duration_min"])
            .groupby("hour")["duration_min"]
            .agg(["mean", "median", "count"])
            .reset_index()
        )
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Bar(
            x=dur_hour["hour"], y=dur_hour["count"],
            name="Sighting Count",
            marker_color="rgba(74,144,226,0.35)",
            hovertemplate="%{x}:00h<br>Count: %{y:,}<extra></extra>"
        ), secondary_y=False)
        fig3.add_trace(go.Scatter(
            x=dur_hour["hour"], y=dur_hour["median"],
            mode="lines+markers",
            name="Median Duration (min)",
            line=dict(color=ACCENT, width=2.5),
            marker=dict(size=6),
            hovertemplate="%{x}:00h<br>Median: %{y:.1f} min<extra></extra>"
        ), secondary_y=True)
        fig3.update_layout(**PLOTLY_LAYOUT,
                           title="⏱️ Count vs Median Duration by Hour",
                           title_font_size=15, height=400,
                           showlegend=True,
                           legend=dict(bgcolor="rgba(0,0,0,0)"))
        fig3.update_yaxes(title_text="Sighting Count",    secondary_y=False,
                          gridcolor=GRID_COL)
        fig3.update_yaxes(title_text="Median Duration (min)", secondary_y=True,
                          gridcolor=GRID_COL)
        fig3.update_xaxes(title_text="Hour (24h)", tickmode="linear", dtick=2)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown(
            f'<div class="insight-card">⏱️ <b>Median duration = '
            f'{df["duration_min"].median():.0f} minutes</b>, but the mean '
            f'is {df["duration_min"].mean():.0f} minutes — indicating a heavy '
            f'right tail from extreme reports. The log-scale histogram confirms '
            f'a roughly log-normal distribution.</div>',
            unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: ANOMALY DETECTION
# ─────────────────────────────────────────────────────────────────────────────
def page_anomaly(df):
    st.markdown('<div class="section-header">🚨 Anomaly Detection</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["📊 Z-Score Method", "📦 IQR Method", "📈 Temporal Spikes"])

    dur_df = df.dropna(subset=["duration_min"]).copy()

    with tab1:
        z_threshold = st.slider("Z-Score Threshold", 2.0, 5.0, 3.0, 0.5,
                                key="z_thresh")

        mu    = dur_df["duration_min"].mean()
        sigma = dur_df["duration_min"].std()
        dur_df["z_score"] = (dur_df["duration_min"] - mu) / sigma
        dur_df["is_anomaly"] = dur_df["z_score"].abs() > z_threshold

        normal   = dur_df[~dur_df["is_anomaly"]]
        outliers = dur_df[dur_df["is_anomaly"]]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records",   f"{len(dur_df):,}")
        col2.metric("Anomalies Found", f"{len(outliers):,}",
                    delta=f"{len(outliers)/len(dur_df)*100:.2f}%")
        col3.metric("Max Duration",    f"{dur_df['duration_min'].max():,.0f} min")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=normal.index[:5000],
            y=normal["duration_min"].iloc[:5000],
            mode="markers",
            marker=dict(size=2, color=ACCENT3, opacity=0.4),
            name=f"Normal ({len(normal):,})",
            hovertemplate="Duration: %{y:.1f} min<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=outliers.index,
            y=outliers["duration_min"],
            mode="markers",
            marker=dict(size=6, color=ACCENT, opacity=0.8, symbol="diamond"),
            name=f"Anomaly (|z|>{z_threshold:.0f}) — {len(outliers):,}",
            hovertemplate=(
                "<b>Anomaly</b><br>Duration: %{y:.1f} min<br>"
                + "Z-score: %{customdata:.1f}<extra></extra>"
            ),
            customdata=outliers["z_score"].abs()
        ))
        fig.add_hline(y=mu + z_threshold * sigma, line_dash="dot",
                      line_color=ACCENT2,
                      annotation_text=f"Upper bound ({z_threshold}σ)",
                      annotation_font_color=ACCENT2)
        style_fig(fig, f"🚨 Duration Anomalies — Z-Score > {z_threshold}", height=420)
        fig.update_layout(yaxis_title="Duration (minutes)", xaxis_title="Record Index",
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

        if not outliers.empty:
            st.markdown("##### 🔍 Top 10 Most Extreme Anomalies")
            top_anomalies = (
                outliers.nlargest(10, "duration_min")
                [["datetime", "city", "country_label", "shape_cleaned",
                  "duration_min", "z_score"]]
                .rename(columns={
                    "datetime": "Date",
                    "city": "City",
                    "country_label": "Country",
                    "shape_cleaned": "Shape",
                    "duration_min": "Duration (min)",
                    "z_score": "Z-Score"
                })
            )
            top_anomalies["Duration (min)"] = top_anomalies["Duration (min)"].round(1)
            top_anomalies["Z-Score"]        = top_anomalies["Z-Score"].round(2)
            st.dataframe(top_anomalies, use_container_width=True, hide_index=True)

    with tab2:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            Q1  = dur_df["duration_min"].quantile(0.25)
            Q3  = dur_df["duration_min"].quantile(0.75)
            IQR = Q3 - Q1
            lower = max(0, Q1 - 1.5 * IQR)
            upper = Q3 + 1.5 * IQR
            iqr_outliers = dur_df[dur_df["duration_min"] > upper]

            fig = go.Figure()
            fig.add_trace(go.Box(
                y=dur_df["duration_min"],
                name="Duration",
                marker_color=ACCENT,
                boxmean=True,
                boxpoints=False,
                hoverinfo="y"
            ))
            style_fig(fig, "📦 Duration Box Plot (with IQR bounds)")
            fig.update_layout(
                yaxis=dict(title="Duration (minutes)", type="log"),
                showlegend=False
            )
            fig.add_hline(y=upper, line_dash="dot", line_color=ACCENT2,
                          annotation_text=f"IQR Upper: {upper:.1f} min",
                          annotation_font_color=ACCENT2)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            sorted_dur = np.sort(dur_df["duration_min"].values)
            ecdf_y     = np.arange(1, len(sorted_dur) + 1) / len(sorted_dur)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=sorted_dur, y=ecdf_y,
                mode="lines",
                line=dict(color=ACCENT3, width=2),
                name="ECDF",
                hovertemplate="Duration: %{x:.1f} min<br>CDF: %{y:.3f}<extra></extra>"
            ))
            fig2.add_vline(x=upper, line_dash="dot", line_color=ACCENT,
                           annotation_text=f"IQR Upper ({upper:.0f} min)",
                           annotation_font_color=ACCENT)
            fig2.add_vline(x=dur_df["duration_min"].median(), line_dash="dot",
                           line_color=ACCENT2,
                           annotation_text="Median",
                           annotation_font_color=ACCENT2)
            style_fig(fig2, "📈 ECDF — Duration Distribution")
            fig2.update_layout(
                xaxis=dict(type="log", title="Duration (minutes, log)"),
                yaxis_title="Cumulative Probability",
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

        # IQR stats
        ci1, ci2, ci3 = st.columns(3)
        ci1.metric("IQR Lower Bound", f"{lower:.1f} min")
        ci2.metric("IQR Upper Bound", f"{upper:.1f} min")
        ci3.metric("IQR Outliers",    f"{len(iqr_outliers):,}  "
                   f"({len(iqr_outliers)/len(dur_df)*100:.1f}%)")

        st.markdown(
            f'<div class="insight-card">📦 <b>IQR analysis</b> flags '
            f'{len(iqr_outliers):,} records as outliers (>{upper:.0f} min). '
            f'The ECDF shows 95% of sightings last under '
            f'{np.percentile(sorted_dur, 95):.0f} minutes, confirming the '
            f'heavy right tail is driven by a small number of extreme reports.'
            f'</div>', unsafe_allow_html=True)

    with tab3:
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            yearly = df.groupby("year").size().reset_index(name="count")
            roll_mean = yearly["count"].rolling(5, center=True).mean()
            roll_std  = yearly["count"].rolling(5, center=True).std()
            upper_spike = roll_mean + 2 * roll_std

            spike_years = yearly[yearly["count"] > upper_spike].dropna()

            fig = go.Figure()
            # Confidence band
            fig.add_trace(go.Scatter(
                x=pd.concat([yearly["year"], yearly["year"][::-1]]),
                y=pd.concat([roll_mean + 2*roll_std,
                              (roll_mean - 2*roll_std)[::-1]]),
                fill="toself",
                fillcolor="rgba(245,166,35,0.1)",
                line=dict(color="rgba(0,0,0,0)"),
                name="±2σ Band", showlegend=True
            ))
            fig.add_trace(go.Scatter(
                x=yearly["year"], y=yearly["count"],
                fill="tozeroy",
                fillcolor="rgba(74,144,226,0.15)",
                line=dict(color=ACCENT3, width=1.5),
                mode="lines", name="Annual Count",
                hovertemplate="<b>%{x}</b><br>%{y:,} sightings<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=yearly["year"], y=roll_mean,
                line=dict(color=ACCENT2, width=2.5, dash="dot"),
                mode="lines", name="5yr Rolling Mean",
                hovertemplate="5yr mean: %{y:,.0f}<extra></extra>"
            ))
            if not spike_years.empty:
                fig.add_trace(go.Scatter(
                    x=spike_years["year"],
                    y=spike_years["count"],
                    mode="markers+text",
                    marker=dict(size=12, color=ACCENT,
                                symbol="star", line=dict(color=DARK_BG, width=1)),
                    text=spike_years["year"].astype(str),
                    textposition="top center",
                    name=f"Spikes ({len(spike_years)})",
                    hovertemplate="<b>%{x}</b> — SPIKE!<br>%{y:,}<extra></extra>"
                ))
            style_fig(fig, "📈 Temporal Spike Detection (Annual)", height=440)
            fig.update_layout(
                xaxis_title="Year", yaxis_title="Sightings",
                legend=dict(bgcolor="rgba(0,0,0,0)", x=0.01, y=0.99)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Monthly spike check for recent years
            recent = df[df["year"] >= 2000]
            monthly_recent = (
                recent.groupby(["year", "month"])
                .size()
                .reset_index(name="count")
            )
            fig2 = px.density_heatmap(
                monthly_recent,
                x="month", y="year",
                z="count",
                color_continuous_scale=[[0, DARK_BG],
                                         [0.3, "#1a0040"],
                                         [0.6, ACCENT],
                                         [1.0, ACCENT2]],
                labels={"month": "Month", "year": "Year", "count": "Sightings"},
                nbinsx=12, nbinsy=15
            )
            fig2.update_layout(
                template="plotly_dark",
                paper_bgcolor=CARD_BG,
                height=440,
                title="🔥 Monthly Density (2000–2014)",
                title_font_size=14,
                margin=dict(l=40, r=20, t=50, b=40),
                xaxis=dict(tickmode="array",
                           tickvals=list(range(1, 13)),
                           ticktext=MONTH_LABELS,
                           gridcolor=GRID_COL),
                yaxis=dict(gridcolor=GRID_COL),
            )
            st.plotly_chart(fig2, use_container_width=True)

        if not spike_years.empty:
            st.markdown("##### 🌟 Detected Spike Years")
            sp_c = st.columns(min(len(spike_years), 5))
            for i, (_, row) in enumerate(spike_years.iterrows()):
                if i < len(sp_c):
                    sp_c[i].metric(str(int(row["year"])),
                                   f"{int(row['count']):,}")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
def page_insights(df):
    st.markdown('<div class="section-header">💡 Key Insights & Conclusions</div>',
                unsafe_allow_html=True)

    # ── Executive dashboard mini-panel (all values guarded against empty) ───
    c1, c2, c3, c4 = st.columns(4)

    yearly_counts = df.groupby("year").size()
    c1.metric("📅 Peak Year",
              str(int(yearly_counts.idxmax())) if len(yearly_counts) > 0 else "N/A")

    hourly_counts = df.groupby("hour").size()
    c2.metric("⏰ Peak Hour",
              f"{int(hourly_counts.idxmax())}:00" if len(hourly_counts) > 0 else "N/A")

    season_counts = df["season"].value_counts()
    c3.metric("🌞 Top Season",
              season_counts.index[0] if len(season_counts) > 0 else "N/A")

    us_states = df[df["country"] == "us"]["state"].value_counts()
    c4.metric("📍 Top US State",
              us_states.index[0].upper() if len(us_states) > 0 else "N/A")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── 6 insights in 2 columns ───────────────────────────────────────────
    left, right = st.columns(2, gap="large")

    insights_left = [
        ("red",   "📈 Internet-Driven Growth",
         "Sightings grew <b>20×</b> after 1994. The internet gave citizens easy "
         "access to NUFORC's online form — data volume reflects reporting "
         "infrastructure, not necessarily sighting frequency."),
        ("blue",  "🌙 Evening Peak at 9 PM",
         "<b>34% of all sightings</b> occur between 20:00–23:00. This aligns "
         "with darkness + wakefulness — the optimal human observation window. "
         "Pre-dawn hours (4–7 AM) have the lowest rates."),
        ("green", "🌞 Summer Dominates",
         "<b>Summer accounts for 33%</b> of annual reports. Warmer weather "
         "encourages outdoor activity and longer evenings, vastly increasing "
         "the number of night-sky observers."),
    ]
    insights_right = [
        ("gold",  "🌍 US Reporting Bias",
         "<b>87% of reports are US-based.</b> This reflects NUFORC's English-"
         "language origins and historical US focus — not necessarily a global "
         "truth about sighting frequency by geography."),
        ("red",   "💡 'Light' Dominates Shapes",
         "<b>21% of all reports describe 'light'</b> as the shape — "
         "consistent with night-time observation where distant objects appear "
         "as undifferentiated light sources regardless of actual form."),
        ("blue",  "🚨 Duration Anomalies",
         "Only <b>0.25% of records</b> qualify as statistical outliers "
         "(Z>3). These extreme reports (hours–days long) warrant manual review "
         "as they likely reflect data entry errors rather than genuine events."),
    ]
    with left:
        for color, title, body in insights_left:
            st.markdown(
                f'<div class="insight-card {color}">'
                f'<b>{title}</b><br>{body}</div>',
                unsafe_allow_html=True)

    with right:
        for color, title, body in insights_right:
            st.markdown(
                f'<div class="insight-card {color}">'
                f'<b>{title}</b><br>{body}</div>',
                unsafe_allow_html=True)

    # ── Summary dashboard ─────────────────────────────────────────────────
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown("#### 📊 Summary Dashboard")

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=["Sightings Per Year", "Top Shapes",
                         "Hour of Day", "Season Distribution",
                         "Top 6 Countries", "Duration Distribution"],
        specs=[[{"type":"xy"}, {"type":"domain"}, {"type":"xy"}],
               [{"type":"xy"}, {"type":"xy"}, {"type":"xy"}]]
    )

    # 1. Year area
    yd = df.groupby("year").size()
    fig.add_trace(go.Scatter(x=yd.index, y=yd.values, fill="tozeroy",
                             fillcolor="rgba(233,69,96,0.2)",
                             line=dict(color=ACCENT, width=1.5),
                             showlegend=False), row=1, col=1)

    # 2. Shapes pie
    sc = df["shape_cleaned"].value_counts().head(6)
    fig.add_trace(go.Pie(labels=[s.title() for s in sc.index],
                         values=sc.values, hole=0.4,
                         marker=dict(colors=COLOR_SEQ),
                         textinfo="percent", showlegend=False), row=1, col=2)

    # 3. Hourly bar
    hd = df.groupby("hour").size()
    fig.add_trace(go.Bar(x=hd.index, y=hd.values,
                         marker=dict(color=hd.values,
                                     colorscale=[[0,"#1a1a4a"],[1,ACCENT]],
                                     showscale=False),
                         showlegend=False), row=1, col=3)

    # 4. Season bar
    sd = df["season"].value_counts()
    fig.add_trace(go.Bar(x=sd.index, y=sd.values,
                         marker_color=[SEASON_COLS.get(s, ACCENT) for s in sd.index],
                         showlegend=False), row=2, col=1)

    # 5. Country bar
    cd = df["country_label"].value_counts().head(6)
    fig.add_trace(go.Bar(x=cd.values, y=cd.index, orientation="h",
                         marker_color=ACCENT3, showlegend=False), row=2, col=2)

    # 6. Duration histogram
    fig.add_trace(go.Histogram(x=df["log_duration"].dropna(), nbinsx=40,
                               marker_color=ACCENT2, showlegend=False), row=2, col=3)

    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=680,
        title=dict(text="🛸 UFO Sightings — Executive Summary Dashboard",
                   font=dict(size=18), x=0.5),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Recommendations ───────────────────────────────────────────────────
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Recommendations")
    r1, r2 = st.columns(2)
    recs_left = [
        ("📡", "Internationalise NUFORC platform with multi-language support "
         "to reduce English-language reporting bias."),
        ("🔍", "Implement duration validation at submission — flag reports "
         ">7 days for mandatory review."),
        ("📅", "Focus monitoring resources on summer evenings (Jul–Sep, "
         "20–23h) for maximum detection probability."),
    ]
    recs_right = [
        ("🗺️",  "Expand geographic coverage by partnering with "
         "international reporting agencies."),
        ("🚨", "Deploy automated anomaly alerts when monthly counts "
         "exceed μ + 2σ of the rolling baseline."),
        ("🤖", "Apply NLP to the comments field to auto-classify and "
         "prioritise credible reports."),
    ]
    with r1:
        for icon, text in recs_left:
            st.markdown(f"**{icon}** {text}")
    with r2:
        for icon, text in recs_right:
            st.markdown(f"**{icon}** {text}")


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def build_sidebar(df):
    with st.sidebar:
        # Title block
        st.markdown("""
        <div style='text-align:center; padding: 0.8rem 0 1rem 0;'>
            <div style='font-size:2.8rem;'>🛸</div>
            <div style='font-size:1.05rem; font-weight:700;
                        color:#e0e0f0; letter-spacing:0.03em;'>
                UFO Intelligence
            </div>
            <div style='font-size:0.72rem; color:#8888aa;
                        margin-top:3px; text-transform:uppercase;
                        letter-spacing:0.1em;'>
                Global Sightings Dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation
        st.markdown('<p class="nav-label">📍 Navigation</p>',
                    unsafe_allow_html=True)
        page = st.radio(
            "",
            options=["🌍 Overview",
                     "📅 Temporal Analysis",
                     "🗺️  Geospatial Analysis",
                     "🛸 Shape & Duration",
                     "🚨 Anomaly Detection",
                     "💡 Key Insights"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Filters
        st.markdown('<p class="nav-label">🎛️ Filters</p>',
                    unsafe_allow_html=True)

        year_min = int(df["year"].min())
        year_max = int(df["year"].max())
        year_range = st.slider(
            "Year Range",
            min_value=year_min, max_value=year_max,
            value=(1990, year_max),
            step=1
        )

        all_countries = sorted(df["country_label"].unique().tolist())
        countries = st.multiselect(
            "Countries",
            options=all_countries,
            default=[],
            placeholder="All countries"
        )

        all_shapes = sorted(df["shape_cleaned"].unique().tolist())
        shapes = st.multiselect(
            "UFO Shapes",
            options=[s.title() for s in all_shapes],
            default=[],
            placeholder="All shapes"
        )
        # Normalise shapes back to lowercase for filtering
        shapes_lower = [s.lower() for s in shapes]

        st.markdown("---")

        # Filter stats
        df_filtered = apply_filters(df, year_range,
                                    countries if countries else None,
                                    shapes_lower if shapes_lower else None)
        pct = len(df_filtered) / len(df) * 100
        st.markdown(
            f'<div style="background:#12122a; border-radius:8px; '
            f'padding:0.7rem; text-align:center;">'
            f'<div style="font-size:1.4rem; font-weight:700; '
            f'color:#e0e0f0;">{len(df_filtered):,}</div>'
            f'<div style="font-size:0.72rem; color:#8888aa; '
            f'text-transform:uppercase; letter-spacing:0.08em;">'
            f'Records ({pct:.0f}% of total)</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.caption("📡 Data: NUFORC Database  \n"
                   "🔬 Built with Streamlit & Plotly")

    return page, df_filtered


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    df_full = load_data()
    page, df = build_sidebar(df_full)

    if len(df) == 0:
        st.warning("⚠️ No records match the current filters. "
                   "Please adjust the sidebar selections.")
        st.stop()

    if page == "🌍 Overview":
        page_overview(df, df_full)
    elif page == "📅 Temporal Analysis":
        page_temporal(df)
    elif page == "🗺️  Geospatial Analysis":
        page_geospatial(df)
    elif page == "🛸 Shape & Duration":
        page_shape_duration(df)
    elif page == "🚨 Anomaly Detection":
        page_anomaly(df)
    elif page == "💡 Key Insights":
        page_insights(df)


if __name__ == "__main__":
    main()