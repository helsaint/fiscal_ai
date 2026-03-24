import json
from openai import OpenAI
from environs import Env
from agents.agents_config import CABINET_BRIEFING_SCHEMA
import inspect
from app.utils.database_cache import check_cache, save_to_cache

env = Env()
env.read_env()
client = OpenAI(api_key=env.str("CHATGPT_API_KEY"))


# Simple bullet point formatting of the signals data
def format_signals(signals):

    formatted = []

    for s in signals:
        formatted.append(
            f"- {s['title']} ({s['severity']})"
        )

    return "\n".join(formatted)

# Creates context for the prompt
def build_cabinet_context(row, fiscal_analysis, review_output):

    context = {
        "ministry": row["ministry"],
        "spend_percentile": row["spend_percentile"],
        "efficiency_rank": row["efficiency_rank"],
        "fiscal_risk_label": row["fiscal_risk_label"],

        # From Fiscal Analyst
        "analysis": fiscal_analysis["analysis"],
        "key_risk_driver": fiscal_analysis["key_risk_driver"],
        "oversight_priority": fiscal_analysis["oversight_priority"],

        # From Expenditure Review
        "review_rationale": review_output["review_rationale"],
        "priority_review_area": review_output["priority_review_area"],
        "recommended_review_action": review_output["recommended_review_action"]
    }

    return context


# Create Prompt
def build_cabinet_prompt(context, signals_text):

    prompt = f"""
You are a senior Treasury official preparing a Cabinet briefing note.

Your task is to present a clear, concise, decision-oriented summary of a ministry's fiscal position.

The audience is Cabinet-level decision-makers. They do not need technical detail. They need clarity on:

- What is happening
- Why it matters
- What action is required

Ministry
--------
{context['ministry']}

Core Position
-------------
Spend Percentile: {context['spend_percentile']}
Efficiency Rank: {context['efficiency_rank']}
Fiscal Risk: {context['fiscal_risk_label']}

Priority Signals
----------------
{signals_text}

Fiscal Assessment
-----------------
{context['analysis']}

Key Risk Driver
---------------
{context['key_risk_driver']}

Oversight Priority
------------------
{context['oversight_priority']}

Expenditure Review Insight
--------------------------
{context['review_rationale']}

Review Focus
------------
{context['priority_review_area']}

Proposed Review Action
----------------------
{context['recommended_review_action']}

Rules
-----
- Be concise and authoritative
- Avoid technical jargon
- Do not repeat inputs verbatim
- Prioritize clarity over completeness
- Prioritize the single most important issue
- Do not include markdown
"""

    return prompt


# Run agent
def generate_cabinet_briefing(
        data_hash,
        row,
        signals,
        fiscal_analysis,
        review_output,
        model="gpt-4o"
        ):
    
    # First we check if the request was made before
    func_name = inspect.currentframe().f_code.co_name
    cached_response = check_cache(data_hash, row['ministry'], func_name)

    # If it exists we pull that instead
    if cached_response:
        return cached_response

    context = build_cabinet_context(row, fiscal_analysis, review_output)
    signals_text = format_signals(signals)
    prompt = build_cabinet_prompt(context, signals_text)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a senior Treasury official."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "cabinet_briefing",
                "schema": CABINET_BRIEFING_SCHEMA
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
            "situation_summary": raw_output,
            "key_issue": "Unavailable",
            "fiscal_implication": "Unavailable",
            "recommended_action": "Unavailable"
        }
        save_to_cache(data_hash, row['ministry'], func_name, parsed)

    return parsed