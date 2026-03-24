from openai import OpenAI
from environs import Env
import streamlit as st
import json
from agents.agents_config import FISCAL_ANALYSIS_SCHEMA
from app.utils.database_cache import check_cache, save_to_cache
import inspect

env = Env()
env.read_env()

client = OpenAI(api_key=env.str("CHATGPT_API_KEY"))

# Create Ministry Context.
# Only use required fields for fiscal analysis

def build_ministry_context(row):

    context = {
        "ministry": row["ministry"],
        "spend_percentile": row["spend_percentile"],
        "efficiency_rank": row["efficiency_rank"],
        "fiscal_risk_score": row["fiscal_risk_score"],
        "fiscal_risk_label": row["fiscal_risk_label"],
        "foreign_dependency": row["foreign_dependency"],
        "capex_ratio": row["capex_ratio_budget_2026"],
        "opex_ratio": row["opex_ratio_budget_2026"],
        "programme_count": row["programme_count"],
        "indicator_count": row["indicator_count"],
        "indicator_outcome_ratio": row["indicator_outcome_ratio"],
        "spend_per_indicator": row["spend_per_indicator"]
    }

    return context


# Creating a bullet structure for signal information
# Allows LLMs to use them properly.
# signals is obtained from the priority_signal_engine
# Gives severity level and text summary "spend_pecentile"
# spend_percentile is a column from master_ministry_fiscal_intelligence.csv

def format_priority_signals(signals):

    formatted = []
    for s in signals:
        formatted.append(
            f"- {s['title']} ({s['severity']}): {s['summary']}"
        )

    return "\n".join(formatted)


# We build an analytical prompt.
# We will use American terms like "Treasury deperatment"
# because most LLMs are probably trained on American data

def build_prompt(context, signals_text):

    prompt = f"""
You are a senior fiscal policy analyst working in a national Treasury department.

Your task is to interpret structured fiscal intelligence about a government ministry.

Your analysis must:
- Maintain a neutral institutional tone
- Be concise and analytical
- Avoid speculation
- Focus on structural fiscal implications

Ministry Context
----------------
Ministry: {context['ministry']}

Spend Percentile: {context['spend_percentile']}
Efficiency Rank: {context['efficiency_rank']}

Fiscal Risk Score: {context['fiscal_risk_score']}
Fiscal Risk Label: {context['fiscal_risk_label']}

Capital Structure
-----------------
Capex Ratio: {context['capex_ratio']}
Opex Ratio: {context['opex_ratio']}
Foreign Financing Dependency: {context['foreign_dependency']}

Operational Structure
---------------------
Programmes: {context['programme_count']}
Indicators: {context['indicator_count']}
Outcome Indicator Ratio: {context['indicator_outcome_ratio']}
Spend per Indicator: {context['spend_per_indicator']}

Priority Signals
----------------
{signals_text}

Task
----
Return a structured fiscal assessment.

Output Format (STRICT)
----------------------
Return ONLY valid JSON with the following fields:

{{
  "analysis": "4–6 sentence fiscal interpretation",
  "key_risk_driver": "single most material fiscal risk driver",
  "oversight_priority": "primary area requiring oversight",
  "recommended_action": "clear, actionable recommendation"
}}

Rules:
- Do not include markdown
- Do not include extra text
- Keep responses concise and formal
"""

    return prompt


# signals is obtained from the priority_signal_engine
# Gives severity level and text summary "spend_pecentile"
# spend_percentile is a column from master_ministry_fiscal_intelligence.csv
# "row" is the line item from master_ministry_fiscal_intelligence.csv 
# for the specific ministry

@st.cache_data(persist="disk")
def generate_fiscal_analysis(data_hash, row, signals, model="gpt-4o"):
    """
    Build structured context
    Format signals: so that LLM can make sense of it.
    Construct prompt
    Query LLM model
    Output a nice json file
    """

    # First we check if the request was made before
    func_name = inspect.currentframe().f_code.co_name
    cached_response = check_cache(data_hash, row['ministry'], func_name)

    # If it exists we pull that instead
    if cached_response:
        st.success("✅ Loaded from Postgres Cache")
        return cached_response

    context = build_ministry_context(row)
    signals_text = format_priority_signals(signals)
    prompt = build_prompt(context, signals_text)

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a senior fiscal analyst."},
        {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "fiscal_analysis",
                "schema": FISCAL_ANALYSIS_SCHEMA
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
            "analysis": raw_output,
            "key_risk_driver": "Unavailable",
            "oversight_priority": "Unavailable",
            "recommended_action": "Unavailable"
        }
        save_to_cache(data_hash, row, parsed)
    
    return parsed