import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.utils.load_csv import load_csv, get_file_hash
from engine.fiscal_core.opex.ministry_intelligence_engine import build_ministry_profile
from app.ui.format_helpers import *
from app.ui.commentary.fiscal_positioning import get_tooltip

from engine.fiscal_core.benchmark_engine import BenchmarkEngine

st.set_page_config(layout="wide")

# --------------------------------------------------
# INITIAL SESSION SETUP
# --------------------------------------------------
if 'df' not in st.session_state:
    st.session_state.df = None

# --------------------------------------------------
# INSTITUTIONAL HEADER
# --------------------------------------------------
st.markdown("""
<div style="padding-top: 10px;">
    <div style="font-size:14px; letter-spacing:1px; color:#555;">
        GOVERNMENT FISCAL INTELLIGENCE SYSTEM - OPEX
    </div>
    <div style="font-size:26px; font-weight:600; margin-top:5px;">
        Ministry Review — Cabinet OPEX Analytical Brief
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# --------------------------------------------------
# MINISTRY SELECTOR
# --------------------------------------------------

# Dummy data for now (replace later with loader)
df_opex = load_csv("BudgetCurrentExpenditure2026_v3.csv")
df_opex_hash = get_file_hash("BudgetCurrentExpenditure2026_v3.csv")
ministries = sorted(df_opex["ministry"].unique())
st.session_state.df = df_opex.copy()

selected_ministry = st.selectbox(
    "Select Ministry",
    ministries
)

st.markdown("---")

# --------------------------------------------------
# EXECUTIVE HEADLINE (Rule-Based Placeholder)
# --------------------------------------------------


profile = build_ministry_profile(st.session_state.df, 
                                 selected_ministry)

st.html("""
<div style="
    font-size:12px;
    letter-spacing:1.5px;
    opacity:0.5;
    margin-bottom:12px;
">
CABINET FISCAL POSITIONING
</div>
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Budget 2026",
        value=f"{format_currency(profile['budgeted_spend_year_0'])}",
        help=get_tooltip("current_budget")
    )

with col2:
    st.metric(
        label="Spend Position",
        value=f"{format_percent(profile['budget_credibility_ratio'])}",
        help=get_tooltip('budget_credibility_ratio')
    )

with col3:
    st.metric(
        label="CAGR",
        value=f"{format_percent(profile['cagr'])}",
        help=get_tooltip("cagr")
    )

st.divider()

st.html("""
<div style="
    font-size:12px;
    letter-spacing:1.5px;
    opacity:0.5;
    margin-bottom:12px;
">
OPEX Growth
</div>
""")

y_formated_bb = [[format_currency(profile['actual_spend_year_2'])], 
                 [format_currency(profile['actual_spend_year_1'])], 
                 [format_currency(profile['budgeted_spend_year_0'])]]

fig_budget_bar = go.Figure(data=[
    go.Bar(
        x=['Actual 2024', 'Actual 2025', 'Budget 2026'],
        y=[profile['actual_spend_year_2'], 
           profile['actual_spend_year_1'],
           profile['budgeted_spend_year_0']
        ],
        customdata=y_formated_bb,
        hovertemplate="<b>%{x}</b>: %{customdata[0]}<extra></extra>"
    )
])

st.plotly_chart(fig_budget_bar, width='stretch')

st.divider()

st.header("Expense Rigidity", help=get_tooltip("personnel_cost_independent_agencies"))

measure_rig = ["relative"]*len(profile['rigidity_distribution'])
measure_rig.append("total")
x_rig = list(profile['rigidity_distribution'])
x_rig.append("total")
y_rig = list(profile['rigidity_distribution'].values())
y_rig.append(0)
text_rig = [format_currency(i) for i in y_rig]
text_rig.append("Total")

fig_rig = go.Figure(go.Waterfall(
    name="20", orientation="v",
    measure=measure_rig,
    x=x_rig,
    textposition="outside",
    text=text_rig,
    y=y_rig,
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig_rig.update_layout(
        title = "Operation costs by spending rigidity",
        showlegend = True
)

st.plotly_chart(fig_rig, width='stretch')

st.divider()

st.html("""
<div style="
    font-size:12px;
    letter-spacing:1.5px;
    opacity:0.5;
    margin-bottom:12px;
">
Distribution of Cost by Economic Group
</div>
""")

measure_egc = ["relative"]*len(profile['economic_group_costs'])
measure_egc.append("Total")
x_egc = list(profile['economic_group_costs'])
x_egc.append("total")
y_egc = list(profile['economic_group_costs'].values())
y_egc.append(0)
text_egc = [format_currency(i) for i in y_egc]
text_egc.append("Total")

fig_egc = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = measure_egc,
    x = x_egc,
    textposition = "outside",
    text = text_egc,
    y = y_egc,
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig_egc.update_layout(
        title = "Costs based on Economic Groups",
        showlegend = True
)

st.plotly_chart(fig_egc, width='stretch')

st.divider()
print(profile)





