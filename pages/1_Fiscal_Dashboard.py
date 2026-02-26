import streamlit as st
import pandas as pd
from app.utils.load_csv import load_csv
import plotly.graph_objects as go
from app.ui.graph_objects_config import RISK_COLORS
import hashlib
from app.ui.format_helpers import *
from app.ui.fiscal_dashboard_tooltip import *
from app.utils.ui import local_css

# Used to generate a unique hash for caching purposes based on the dataframe content
def get_hash(df):
    # Create a unique MD5 hash based on the dataframe content
    return hashlib.md5(pd.util.hash_pandas_object(df).values).hexdigest()

# --------------------------------------------------
# Load Main Dataset
# --------------------------------------------------

df_mfi = load_csv("master_ministry_fiscal_intelligence.csv")

# --------------------------------------------------
# Load CSS
# --------------------------------------------------

local_css("style.css")

# --------------------------------------------------
# Header
# --------------------------------------------------

st.set_page_config(
    page_title="Fiscal Dashboard",
    layout="wide"
)

st.title("Fiscal Intelligence Dashboard")
st.markdown("Executive overview of fiscal exposure and ministry risk positioning.")
st.divider()

# --------------------------------------------------
# Compute executive summary metrics
# --------------------------------------------------

total_spend_2026 = df_mfi["total_spend_2026"].sum()
capex_2026 = df_mfi["capex_2026"].sum()
opex_2026 = df_mfi["opex_2026"].sum()

weighted_risk_score = (
    (df_mfi["fiscal_risk_score"] * df_mfi["total_spend_2026"]).sum()
    / df_mfi["total_spend_2026"].sum()
)

budget_pressure_pct = (
    df_mfi["budget_pressure_flag"].sum() / len(df_mfi)
) * 100

high_performer_pct = (
    df_mfi["high_performer_flag"].sum() / len(df_mfi)
) * 100

# --------------------------------------------------
# Fiscal Overview Cards
# --------------------------------------------------

st.markdown("## National Fiscal Overview – FY2026")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_spend_2026_formatted = format_currency(total_spend_2026)
    capex_2026_formatted = format_currency(capex_2026)
    opex_2026_formatted = format_currency(opex_2026)
    help_text = "Capex: " + capex_2026_formatted + " | Opex: " + opex_2026_formatted
    st.markdown(f"""
        <div class="metric-card">
            <span class="tooltip-text">{help_text}</span>
            <div class="metric-label">Total Spend (2026)</div>
            <div class="metric-value">{total_spend_2026_formatted}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    help_text = tooltip_classify_risk(weighted_risk_score)
    st.markdown(f"""
        <div class="metric-card">
            <span class="tooltip-text">{help_text}</span>
            <div class="metric-label">Weighted Risk Score</div>
            <div class="metric-value">{weighted_risk_score:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    help_text = tooltip_budget_pressure_percent(budget_pressure_pct)
    st.markdown(f"""
        <div class="metric-card">
            <span class="tooltip-text">{help_text}</span>
            <div class="metric-label">Budget Pressure (%)</div>
            <div class="metric-value">{budget_pressure_pct:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    #st.metric("High Performer (%)", f"{high_performer_pct:.1f}%")
    help_text = "Best performing agency: "
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High Performer (%)</div>
            <div class="metric-value">{high_performer_pct:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# Expenditure Composition
# --------------------------------------------------
st.markdown("### Expenditure Composition")
total_opex = df_mfi["opex_2026"].sum()
total_gov_capex = df_mfi["gov_capex_budget_2026"].sum()
total_foreign_capex = df_mfi["foreign_capex_budget_2026"].sum()

total_expenditure = total_opex + total_gov_capex + total_foreign_capex

extra_metadata = [
    [format_currency(total_opex), 
     df_mfi.loc[df_mfi["opex_2026"].idxmax()].loc['ministry'], 
     format_currency(df_mfi.loc[df_mfi["opex_2026"].idxmax()].loc['opex_2026'])],
    [format_currency(total_gov_capex), 
     df_mfi.loc[df_mfi["gov_capex_budget_2026"].idxmax()].loc['ministry'], 
     format_currency(
         df_mfi.loc[df_mfi["gov_capex_budget_2026"].idxmax()].loc['gov_capex_budget_2026']
         )],
    [format_currency(total_foreign_capex), 
     df_mfi.loc[df_mfi["foreign_capex_budget_2026"].idxmax()].loc['ministry'], 
     format_currency(
         df_mfi.loc[
             df_mfi["foreign_capex_budget_2026"].idxmax()].loc['foreign_capex_budget_2026']
     )]
]

print(extra_metadata[0:2:1])

fig_exp_comp = go.Figure(data=[go.Pie(
    labels=[
        "Operational Expenditure",
        "Domestic Capital Investment",
        "Foreign-Funded Capital Investment"
    ],
    values=[
        total_opex,
        total_gov_capex,
        total_foreign_capex
    ],
    hole=0.6,
    textinfo="percent",
    marker=dict(
        colors=["#102a43", "#486581", "#829ab1"]
    ),
    customdata=extra_metadata,
    hovertemplate=(
        "<b> Budgeted: </b> %{customdata[0][0]}<br>" +
        "<b> Highest Spend Ministry: </b> %{customdata[0][1]}<br>" +
        "<b> Ministry Spend: </b> %{customdata[0][2]}<br>"
    )
)])

fig_exp_comp.update_layout(
    title="FY2026 Expenditure Composition",
    height=420,
    margin=dict(l=20, r=20, t=60, b=20),
    showlegend=True
)

st.plotly_chart(fig_exp_comp, width='stretch', key='exp_comp_chart')
opex_ratio = total_opex / total_expenditure * 100
capex_ratio = (total_gov_capex + total_foreign_capex) / total_expenditure * 100
foreign_capex_ratio = total_foreign_capex / total_expenditure * 100

st.caption(
    f"Operational expenditure accounts for {opex_ratio:.1f}% of total FY2026 spending. "
    f"Capital investment represents {capex_ratio:.1f}%, of which "
    f"{foreign_capex_ratio:.1f}% is foreign-funded."
)

# --------------------------------------------------
# Expenditure Evolution
# --------------------------------------------------
st.markdown("### Expenditure Composition Evolution")
# --- Aggregate OPEX ---
opex_2024 = df_mfi["opex_2024"].sum()
opex_2025 = df_mfi["opex_2025"].sum()
opex_2026 = df_mfi["opex_2026"].sum()

# --- Aggregate Domestic CAPEX ---
gov_capex_2024 = df_mfi["gov_capex_actual_2024"].sum()
gov_capex_2025 = df_mfi["gov_capex_actual_2025"].sum()
gov_capex_2026 = df_mfi["gov_capex_budget_2026"].sum()

# --- Aggregate Foreign CAPEX ---
foreign_capex_2024 = df_mfi["foreign_capex_actual_2024"].sum()
foreign_capex_2025 = df_mfi["foreign_capex_actual_2025"].sum()
foreign_capex_2026 = df_mfi["foreign_capex_budget_2026"].sum()

# --- Ratios ---

total_2024 = opex_2024 + gov_capex_2024 + foreign_capex_2024
total_2025 = opex_2025 + gov_capex_2025 + foreign_capex_2025
total_2026 = opex_2026 + gov_capex_2026 + foreign_capex_2026

capex_ratio_2024 = (gov_capex_2024 + foreign_capex_2024) / total_2024 * 100
capex_ratio_2025 = (gov_capex_2025 + foreign_capex_2025) / total_2025 * 100
capex_ratio_2026 = (gov_capex_2026 + foreign_capex_2026) / total_2026 * 100

# --- Growth Rates ---
growth_2025 = ((total_2025 - total_2024) / total_2024) * 100
growth_2026 = ((total_2026 - total_2025) / total_2025) * 100

# 2024 has no prior year
growth_rates = [None, growth_2025, growth_2026]

fig_trend = go.Figure()

years = ["2024 (Actual)", "2025 (Actual)", "2026 (Budget)"]

extra_metadata= [
    [format_currency(opex_2024), format_currency(opex_2025), 
     format_currency(opex_2026)],
    [format_currency(gov_capex_2024), format_currency(gov_capex_2025), 
     format_currency(gov_capex_2026)],
    [format_currency(foreign_capex_2024), format_currency(foreign_capex_2025), 
     format_currency(foreign_capex_2026)]
]

print(extra_metadata[0:2:1])

# --- Stacked Bars ---
fig_trend.add_trace(go.Bar(
    name="Operational Expenditure",
    x=years,
    y=[opex_2024, opex_2025, opex_2026],
    marker_color="#102a43",
    customdata=list(zip(years,extra_metadata[0])),
    hovertemplate=(
        "<b></b>%{customdata}<br>"
    ),
))

fig_trend.add_trace(go.Bar(
    name="Domestic Capital Investment",
    x=years,
    y=[gov_capex_2024, gov_capex_2025, gov_capex_2026],
    marker_color="#486581",
    customdata=list(zip(years,extra_metadata[1])),
    hovertemplate=(
        "<b></b>%{customdata}<br>"
    ),
))

fig_trend.add_trace(go.Bar(
    name="Foreign-Funded Capital Investment",
    x=years,
    y=[foreign_capex_2024, foreign_capex_2025, foreign_capex_2026],
    marker_color="#829ab1",
    customdata=list(zip(years,extra_metadata[2])),
    hovertemplate=(
        "<b></b>%{customdata}<br>"
    ),
))

# --- Capital Intensity Line (Secondary Axis) ---
fig_trend.add_trace(go.Scatter(
    name="Capital Intensity (%)",
    x=years,
    y=[capex_ratio_2024, capex_ratio_2025, capex_ratio_2026],
    mode="lines+markers",
    line=dict(color="#243b53", width=3),
    marker=dict(size=8),
    yaxis="y2"
))

# --- Total Expenditure Growth Line ---
fig_trend.add_trace(go.Scatter(
    name="Total Expenditure Growth (%)",
    x=years,
    y=growth_rates,
    mode="lines+markers",
    line=dict(color="#334e68", width=2, dash="dash"),
    marker=dict(size=7),
    yaxis="y2"
))


fig_trend.update_layout(
    barmode="stack",
    title="Expenditure Structure Evolution: 2024–2026",
    height=520,
    margin=dict(l=20, r=20, t=60, b=40),
    xaxis_title="Fiscal Year",
    yaxis=dict(
        title="Total Expenditure"
    ),
    yaxis2=dict(
        title="Capital Intensity (%)",
        overlaying="y",
        side="right",
        range=[0, 100],
        showgrid=False
    ),
    legend_title="Expenditure Type"
)

st.plotly_chart(fig_trend, width='stretch', key='exp_evo_chart')

st.caption(
    f"Capital intensity increased from {capex_ratio_2024:.1f}% (2024) "
    f"to {capex_ratio_2025:.1f}% (2025), "
    f"with the FY2026 budget projecting {capex_ratio_2026:.1f}%."
)