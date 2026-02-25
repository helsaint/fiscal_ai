import streamlit as st
import pandas as pd
from app.utils.load_csv import load_csv
import plotly.graph_objects as go
from app.ui.graph_objects_config import RISK_COLORS
import hashlib
from app.ui.format_helpers import *
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
    #st.metric("Total Spend (2026)", format_currency(total_spend_2026))
    total_spend_2026_formatted = format_currency(total_spend_2026)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Spend (2026)</div>
            <div class="metric-value">{total_spend_2026_formatted}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("Weighted Risk Score", f"{weighted_risk_score:.2f}")

with col3:
    st.metric("Budget Pressure (%)", f"{budget_pressure_pct:.1f}%")

with col4:
    st.metric("High Performer (%)", f"{high_performer_pct:.1f}%")