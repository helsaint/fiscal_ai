import json
from openai import OpenAI
from environs import Env
from agents.agents_config import EXPENDITURE_REVIEW_SCHEMA
from app.utils.database_cache import check_cache, save_to_cache
import streamlit as st
from app.utils.database_cache import check_cache, save_to_cache
import inspect

env = Env()
env.read_env()
client = OpenAI(api_key=env.str("CHATGPT_API_KEY"))


# ==========================================================
# 1. BUILD REVIEW CONTEXT
# ==========================================================

def build_review_context(row):

    context = {
        "ministry": row["ministry"],
        "spend_percentile": row["spend_percentile"],
        "efficiency_rank": row["efficiency_rank"],
        "fiscal_risk_label": row["fiscal_risk_label"],
        "capex_ratio": row["capex_ratio_budget_2026"],
        "foreign_dependency": row["foreign_dependency"],
        "programme_count": row["programme_count"],
        "indicator_count": row["indicator_count"],
        "indicator_outcome_ratio": row["indicator_outcome_ratio"],
        "spend_per_indicator": row["spend_per_indicator"],
        "capex_pressure": row["capex_pressure"],
        "foreign_risk": row["foreign_risk"],
        "weak_outcomes": row["weak_outcomes"],
        "low_efficiency": row["low_efficiency"]
    }

    return context


# ==========================================================
# 2. FORMAT SIGNALS
# ==========================================================

def format_signals(signals):

    formatted = []

    for s in signals:
        formatted.append(
            f"- {s['title']} ({s['severity']}): {s['summary']}"
        )

    return "\n".join(formatted)


# ==========================================================
# 3. BUILD EXPENDITURE REVIEW PROMPT
# ==========================================================

def build_review_prompt(context, signals_text):

    prompt = f"""
You are a senior expenditure review analyst working in a national Treasury department.

Your task is to determine whether a ministry should be subject to expenditure review and what areas of spending warrant closer examination.

Maintain an institutional analytical tone. Focus on fiscal management and resource efficiency.

Ministry Context
----------------
Ministry: {context['ministry']}

Spend Percentile: {context['spend_percentile']}
Efficiency Rank: {context['efficiency_rank']}
Fiscal Risk Label: {context['fiscal_risk_label']}

Capital Structure
-----------------
Capex Ratio: {context['capex_ratio']}
Foreign Financing Dependency: {context['foreign_dependency']}
Capital Pressure Flag: {context['capex_pressure']}

Operational Structure
---------------------
Programmes: {context['programme_count']}
Indicators: {context['indicator_count']}
Outcome Indicator Ratio: {context['indicator_outcome_ratio']}
Spend per Indicator: {context['spend_per_indicator']}

Performance Flags
-----------------
Low Efficiency: {context['low_efficiency']}
Weak Outcomes: {context['weak_outcomes']}
Foreign Risk: {context['foreign_risk']}

Priority Signals
----------------
{signals_text}

Task
----
Assess whether the ministry warrants expenditure review attention.

Output Format (STRICT JSON)
---------------------------

Return ONLY valid JSON with the following fields:

{{
  "review_rationale": "2-3 sentence explanation of why review may be warranted",
  "priority_review_area": "specific area where review should focus",
  "efficiency_opportunity": "potential opportunity to improve spending efficiency",
  "recommended_review_action": "clear action such as targeted expenditure review or programme audit"
}}

Rules
-----
- Do not include markdown
- Do not include commentary outside JSON
- Keep language concise and institutional
"""

    return prompt


# ==========================================================
# 4. RUN AGENT
# ==========================================================
@st.cache_data(persist="disk")
def generate_expenditure_review(data_hash, row, signals, model="gpt-4o"):

    # First we check if the request was made before
    func_name = inspect.currentframe().f_code.co_name
    cached_response = check_cache(data_hash, row['ministry'], func_name)

    # If it exists we pull that instead
    if cached_response:
        st.success("✅ Loaded from Postgres Cache")
        return cached_response

    context = build_review_context(row)
    signals_text = format_signals(signals)
    prompt = build_review_prompt(context, signals_text)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a senior public expenditure analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "expenditure_review",
                "schema": EXPENDITURE_REVIEW_SCHEMA
            }
        }
    )

    raw_output = response.choices[0].message.content

    try:
        parsed = json.loads(raw_output)
        save_to_cache(data_hash, row['ministry'], func_name, parsed)
        return parsed
    except json.JSONDecodeError:
        parsed = {
            "review_rationale": raw_output,
            "priority_review_area": "Unavailable",
            "efficiency_opportunity": "Unavailable",
            "recommended_review_action": "Unavailable"
        }
        save_to_cache(data_hash, row['ministry'], func_name, parsed)


    return parsed