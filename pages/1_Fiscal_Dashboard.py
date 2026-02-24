import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from app.ui.graph_objects_config import RISK_COLORS

st.set_page_config(
    page_title="Fiscal Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("Fiscal Intelligence Dashboard")
st.markdown("Executive overview of fiscal exposure and ministry risk positioning.")
st.divider()

# --------------------------------------------------
# Dummy Data (Temporary)
# --------------------------------------------------

data = {
    "Ministry": [
        "Health",
        "Transport",
        "Education",
        "Public Works",
        "Energy",
        "Defense"
    ],
    "Total Spend (2026)": [120, 95, 110, 75, 130, 160],
    "Risk Level": ["High", "Moderate", "Low", "Moderate", "High", "Low"],
    "Efficiency Score": [52, 68, 81, 63, 49, 77]
}

df = pd.DataFrame(data)

# --------------------------------------------------
# Key Indicators (Top Row)
# --------------------------------------------------

# --------------------------------------------------
# Executive Summary Cards
# --------------------------------------------------

st.subheader("Executive Summary")

total_exposure = df["Total Spend (2026)"].sum()
high_risk_count = (df["Risk Level"] == "High").sum()
avg_eff = round(df["Efficiency Score"].mean(), 1)
total_ministries = len(df)

col1, col2, col3, col4 = st.columns(4)

def summary_card(title, value):
    with st.container(border=True):
        st.markdown(f"**{title.upper()}**")
        st.markdown(f"<h2 style='margin-top: 0;'>{value}</h2>", unsafe_allow_html=True)

with col1:
    summary_card("Total Fiscal Exposure", f"{total_exposure} B")

with col2:
    summary_card("High-Risk Ministries", high_risk_count)

with col3:
    summary_card("Average Efficiency Index", avg_eff)

with col4:
    summary_card("Total Ministries", total_ministries)

# --------------------------------------------------
# Ministry Summary Table
# --------------------------------------------------

st.subheader("Ministry Risk Overview")

st.dataframe(
    df,
    width='stretch',
    hide_index=True
)

st.divider()

# --------------------------------------------------
# Risk Distribution (Controlled)
# --------------------------------------------------

st.subheader("Risk Distribution")

risk_counts = df["Risk Level"].value_counts()

fig_risk = go.Figure()

for risk_level in ["High", "Moderate", "Low"]:
    if risk_level in risk_counts.index:
        fig_risk.add_trace(
            go.Bar(
                x=[risk_level],
                y=[risk_counts[risk_level]],
                name=risk_level,
                marker=dict(color=RISK_COLORS[risk_level]),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Ministries: %{y}<extra></extra>"
                )
            )
        )

fig_risk.update_layout(
    showlegend=False,
    xaxis_title="Risk Classification",
    yaxis_title="Number of Ministries",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=40, r=20, t=40, b=40),
    font=dict(size=14)
)

fig_risk.update_xaxes(showgrid=False)
fig_risk.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")

st.plotly_chart(fig_risk, uwidth='stretch')

# --------------------------------------------------
# Efficiency Relative to Fiscal Exposure
# --------------------------------------------------

st.subheader("Efficiency Relative to Fiscal Exposure")

fig_scatter = go.Figure()

for risk_level in ["High", "Moderate", "Low"]:
    subset = df[df["Risk Level"] == risk_level]

    fig_scatter.add_trace(
        go.Scatter(
            x=subset["Total Spend (2026)"],
            y=subset["Efficiency Score"],
            mode="markers",
            name=risk_level,
            marker=dict(
                size=12,
                color=RISK_COLORS[risk_level],
                line=dict(width=0.5, color="black")
            ),
            text=subset["Ministry"],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Spend: %{x} B<br>"
                "Efficiency: %{y}<br>"
                "Risk: " + risk_level +
                "<extra></extra>"
            )
        )
    )

fig_scatter.update_layout(
    xaxis_title="Total Spend (2026)",
    yaxis_title="Efficiency Score",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=40, r=20, t=40, b=40),
    legend_title="Risk Level",
    font=dict(size=14)
)

fig_scatter.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
fig_scatter.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")

st.plotly_chart(fig_scatter, width='stretch')