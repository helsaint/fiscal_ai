import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.utils.load_csv import load_csv, get_file_hash
from engine.fiscal_core.ministry_review.ministry_intelligence_engine import build_ministry_profile
from engine.fiscal_core.ministry_review.cabinet_framing_engine import generate_executive_headline
from app.ui.format_helpers import *
from app.ui.graph_objects_config import STABILITY_COLOR
from engine.fiscal_core.ministry_review.commentary.fiscal_positioning import get_tooltip
from engine.fiscal_core.ministry_review.priority_signal_engine import build_priority_signals
from agents.fiscal_analyst_agent_ministry import generate_fiscal_analysis
from agents.expenditure_review_agent_ministry import generate_expenditure_review
from agents.cabinet_briefing_agent_ministry import generate_cabinet_briefing

from engine.fiscal_core.benchmark_engine import BenchmarkEngine

st.set_page_config(layout="wide")

# --------------------------------------------------
# INITIAL SESSION SETUP
# --------------------------------------------------
if 'fiscal_analysis_output' not in st.session_state:
    st.session_state.fiscal_analysis_output = None
if 'review_output' not in st.session_state:
    st.session_state.review_output = None
if 'cabinet_briefing_output' not in st.session_state:
    st.session_state.cabinet_briefing_output = None
if 'df' not in st.session_state:
    st.session_state.df = None

# --------------------------------------------------
# INSTITUTIONAL HEADER
# --------------------------------------------------

st.markdown("""
<div style="padding-top: 10px;">
    <div style="font-size:14px; letter-spacing:1px; color:#555;">
        GOVERNMENT FISCAL INTELLIGENCE SYSTEM
    </div>
    <div style="font-size:26px; font-weight:600; margin-top:5px;">
        Ministry Review — Cabinet Analytical Brief
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# --------------------------------------------------
# MINISTRY SELECTOR
# --------------------------------------------------

# Dummy data for now (replace later with loader)
df_summary = load_csv("master_ministry_fiscal_intelligence.csv")
df_summary_hash = get_file_hash("master_ministry_fiscal_intelligence.csv")
ministries = sorted(df_summary["ministry"].unique())
st.session_state.df = df_summary.copy()

selected_ministry = st.selectbox(
    "Select Ministry",
    ministries
)

st.markdown("---")

# --------------------------------------------------
# EXECUTIVE HEADLINE (Rule-Based Placeholder)
# --------------------------------------------------

ministry_data = df_summary[df_summary["ministry"] == selected_ministry].iloc[0]

profile = build_ministry_profile(df_summary, selected_ministry)
framing = generate_executive_headline(profile)

test_benchmark_engine = BenchmarkEngine(df_summary)
# --------------------------------------------------
# EXECUTIVE INTELLIGENCE PANEL
# --------------------------------------------------

headline = framing["headline"]
posture = framing["posture"]
risk_score = format_percent(framing["risk_score"])
risk_label = framing["risk_label"]
spend_percentile = format_percent_round(100*framing["spend_percentile"])
efficiency_rank = framing["efficiency_rank"]

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
        label="Composite Risk Score",
        value=f"{risk_score}",
        help=get_tooltip("fiscal_risk_score")
    )

with col2:
    st.metric(
        label="Spend Position",
        value=f"{spend_percentile}th Percentile",
        help=get_tooltip("spend_percentile")
    )

with col3:
    st.metric(
        label="Efficiency Rank",
        value=str(efficiency_rank),
        help=get_tooltip("efficiency_rank")
    )

st.divider()
st.markdown("### Prirority Signals ###")
signals = build_priority_signals(profile)

col1, col2 = st.columns(2)

for i, signal in enumerate(signals):
    target_col = col1 if i % 2 == 0 else col2

    if signal["severity"] == "High":
        accent = "rgba(255,90,90,0.6)"
    elif signal["severity"] == "Moderate":
        accent = "rgba(255,180,0,0.6)"
    else:
        accent = "rgba(255,255,255,0.08)"

    with target_col:
        st.html(f"""
        <div style="
            border-left:4px solid {accent};
            padding:18px;
            margin-bottom:18px;
            border-radius:6px;
            border:1px solid rgba(255,255,255,0.05);
        ">
            <div style="font-weight:600; font-size:16px; margin-bottom:8px;">
                {signal['title']}
            </div>
            <div style="font-size:13px; opacity:0.6; text-transform:uppercase; margin-bottom:6px;">
                {signal['severity']}
            </div>
            <div style="font-size:14px; opacity:0.85;">
                {signal['summary']}
            </div>
        </div>
        """)

# --------------------------------------------------
# Structured Fiscal Profile
# --------------------------------------------------

st.divider()
st.markdown("## Structured Fiscal Profile ##")
row = df_summary[df_summary["ministry"] == selected_ministry].iloc[0]
opex_2024 = row["opex_2024"]
opex_2025 = row["opex_2025"]
opex_2026 = row["opex_2026"]

capex_2024 = row["capex_2024"]
capex_2025 = row["capex_2025"]
capex_2026 = row["capex_2026"]

total_2024 = row["opex_2024"] + row["capex_2024"]
total_2025 = row["opex_2025"] + row["capex_2025"]
total_2026 = row["opex_2026"] + row["capex_2026"]

growth = ((total_2026 - total_2024) / total_2024) * 100
fiscal_table = pd.DataFrame({
    "Year": ["2024", "2025", "2026"],
    "Operational Expenditure": [opex_2024, opex_2025, opex_2026],
    "Capital Expenditure": [capex_2024, capex_2025, capex_2026],
    "Total Expenditure": [total_2024, total_2025, total_2026]
})

st.markdown("---")
st.markdown("### Fiscal Scale & Trajectory")

st.dataframe(
    fiscal_table.style.format({
        "Operational Expenditure": "${:,.0f}",
        "Capital Expenditure": "${:,.0f}",
        "Total Expenditure": "${:,.0f}",
    }),
    width='stretch',
    hide_index=True
)

st.markdown(
    f"""
    <div style="margin-top:8px; opacity:0.75;">
    2024–2026 expenditure growth: <b>{growth:.1f}%</b>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend 2024", format_currency(total_2024))
col2.metric("Total Spend 2025",format_currency(total_2025))
col3.metric("Total Spend 2026", format_currency(total_2026))
col4.metric("Growth 2024–2026", f"{growth:.1f}%")

st.markdown("### Expenditure Composition")
capex_ratio = row["capex_ratio_budget_2026"] * 100
opex_ratio = row["opex_ratio_budget_2026"] * 100

col1, col2 = st.columns(2)

with col1:
    st.metric("Capital Expenditure Ratio (2026)", f"{capex_ratio:.1f}%")

with col2:
    st.metric("Operational Expenditure Ratio (2026)", f"{opex_ratio:.1f}%")

st.progress(capex_ratio / 100)
st.caption("Capital Investment Share of Total Budget")

st.markdown("### Capital Financing Structure")

gov_capex = row["gov_capex_budget_2026"]
foreign_capex = row["foreign_capex_budget_2026"]
foreign_share = (foreign_capex / (foreign_capex + gov_capex)) * 100
col1, col2, col3 = st.columns(3)
col1.metric("Gov-Financed Capex", format_currency(gov_capex))
col2.metric("Foreign-Financed Capex", format_currency(foreign_capex))
col3.metric("External Financing Share", f"{foreign_share:.1f}%")

st.markdown("### Programme & Indicator Structure")

programme_count = row["programme_count"]
indicator_count = row["indicator_count"]
outcome_ratio = row["indicator_outcome_ratio"] * 100
spend_per_indicator = row["spend_per_indicator"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Programmes", programme_count)
col2.metric("Indicators", indicator_count)
col3.metric("Outcome Indicator Ratio", f"{outcome_ratio:.1f}%")
col4.metric("Spend per Indicator", format_currency(spend_per_indicator))

st.markdown("### Relative Ministry Positioning")
viz_df = df_summary.copy()
efficiency_mid = viz_df["efficiency_rank"].median()
spend_mid = 0.5

viz_df["total_spend"] = viz_df["opex_2026"] + viz_df["capex_2026"]
size_scale = viz_df["total_spend"] / viz_df["total_spend"].max() * 60
fig = go.Figure()
for i, row in viz_df.iterrows():
    
    fig.add_trace(
        go.Scatter(
            x=[row["efficiency_rank"]],
            y=[row["spend_percentile"]],
            mode="markers",
            marker=dict(
                size=size_scale[i],
                color=STABILITY_COLOR.get(row["fiscal_risk_label"], "#888"),
                opacity=0.7,
                line=dict(width=1, color="rgba(255,255,255,0.2)")
            ),
            name=row["ministry"],
            text=[row["ministry"]],
            hovertemplate=
                "<b>%{text}</b><br>" +
                "Efficiency Rank: %{x}<br>" +
                "Spend Percentile: %{y}<extra></extra>",
            showlegend=False
        )
    )

selected = viz_df[viz_df["ministry"] == selected_ministry].iloc[0]

fig.add_trace(
    go.Scatter(
        x=[selected["efficiency_rank"]],
        y=[selected["spend_percentile"]],
        mode="markers",
        marker=dict(
            size=22,
            color="white",
            line=dict(width=3, color="white")
        ),
        name=selected_ministry,
        hoverinfo="skip"
    )
)

fig.add_shape(
    type="line",
    x0=efficiency_mid,
    x1=efficiency_mid,
    y0=0,
    y1=1,
    line=dict(
        color="rgba(255,255,255,0.15)",
        width=1,
        dash="dash"
    )
)

fig.add_shape(
    type="line",
    x0=viz_df["efficiency_rank"].min(),
    x1=viz_df["efficiency_rank"].max(),
    y0=spend_mid,
    y1=spend_mid,
    line=dict(
        color="rgba(255,255,255,0.15)",
        width=1,
        dash="dash"
    )
)

fig.add_annotation(
    x=efficiency_mid * 0.5,
    y=0.8,
    text="High Spend / Strong Efficiency",
    showarrow=False,
    font=dict(size=11, color="rgba(255,255,255,0.45)")
)

fig.add_annotation(
    x=efficiency_mid * 1.5,
    y=0.8,
    text="High Spend / Weak Efficiency",
    showarrow=False,
    font=dict(size=11, color="rgba(255,255,255,0.45)")
)

fig.add_annotation(
    x=efficiency_mid * 0.5,
    y=0.2,
    text="Low Spend / Strong Efficiency",
    showarrow=False,
    font=dict(size=11, color="rgba(255,255,255,0.45)")
)

fig.add_annotation(
    x=efficiency_mid * 1.5,
    y=0.2,
    text="Low Spend / Weak Efficiency",
    showarrow=False,
    font=dict(size=11, color="rgba(255,255,255,0.45)")
)

st.plotly_chart(fig, width='stretch')

st.divider()


if (st.button("Generate Fiscal Analysis")
    and 
    st.session_state.fiscal_analysis_output == None):

    row = df_summary[df_summary["ministry"] == selected_ministry].iloc[0]

    fiscal_analysis = generate_fiscal_analysis(st.session_state.df,
        df_summary_hash, row, signals)
    st.session_state.fiscal_analysis_output = fiscal_analysis
    
if st.session_state.fiscal_analysis_output:
    st.markdown("### Fiscal Interpretation")
    st.write(st.session_state.fiscal_analysis_output["analysis"])

    st.markdown("### Fiscal Opportunit")
    st.write(st.session_state.fiscal_analysis_output["fiscal_opportunity"])

    st.markdown("### Key Risk Driver")
    st.write(st.session_state.fiscal_analysis_output["key_risk_driver"])

    st.markdown("### Oversight Priority")
    st.write(st.session_state.fiscal_analysis_output["oversight_priority"])

    st.markdown("### Compatative Position")
    st.write(st.session_state.fiscal_analysis_output["comparative_position"])

    st.markdown("### Recommended Action")
    st.write(st.session_state.fiscal_analysis_output["recommended_action"])

st.divider()

if st.button("Generate Expenditure Review"):

    row = df_summary[df_summary["ministry"] == selected_ministry].iloc[0]

    review_output = generate_expenditure_review(df_summary_hash, row, signals)
    st.session_state.review_output = review_output

if st.session_state.review_output:
    st.markdown("### Expenditure Review Assessment")

    st.markdown("**Review Rationale**")
    st.write(st.session_state.review_output["review_rationale"])

    st.markdown("**Priority Review Area**")
    st.write(st.session_state.review_output["priority_review_area"])

    st.markdown("**Efficiency Opportunity**")
    st.write(st.session_state.review_output["efficiency_opportunity"])

    st.markdown("**Recommended Review Action**")
    st.write(st.session_state.review_output["recommended_review_action"])

st.divider()

if st.button("Generate Cabinet Briefing"):

    row = df_summary[df_summary["ministry"] == selected_ministry].iloc[0]
    if (
        not st.session_state.fiscal_analysis_output
        ) and (
            not st.session_state.review_output
            ):
        st.error("Generate the above two reports first")
    else:
        briefing = generate_cabinet_briefing(
            df_summary_hash,
            row,
            signals,
            st.session_state.fiscal_analysis_output,
            st.session_state.review_output
        )
        st.session_state.cabinet_briefing_output = briefing

if st.session_state.cabinet_briefing_output:        
    st.markdown("### Cabinet Briefing")
    st.markdown("**Situation Summary**")
    st.write(st.session_state.cabinet_briefing_output["situation_summary"])
    st.markdown("**Key Issue**")
    st.write(st.session_state.cabinet_briefing_output["key_issue"])
    st.markdown("**Fiscal Implication**")
    st.write(st.session_state.cabinet_briefing_output["fiscal_implication"])
    st.markdown("**Recommended Action**")
    st.write(st.session_state.cabinet_briefing_output["recommended_action"])
    
