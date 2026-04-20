# Create tooltip hover data

FIELD_METADATA = {
    "fiscal_risk_score": {
        "label": "Composite Risk Score",
        "description": "Composite measure of fiscal vulnerability derived from structural, volatility, and delivery risk components.",
        "interpretation": "Higher scores indicate greater exposure to fiscal instability."
    },

    "spend_percentile": {
        "label": "Spend Position",
        "description": "Percentile ranking of total ministry expenditure relative to peer ministries.",
        "interpretation": "Higher percentile indicates larger fiscal footprint."
    },

    "efficiency_rank": {
        "label": "Efficiency Rank",
        "description": "Relative efficiency ranking compared to other ministries.",
        "interpretation": "Lower rank indicates stronger relative efficiency performance."
    },

    "current_budget": {
        "label": "Current Operational Budget",
        "description": "Operational Budget for this year",
        "interpretation": "Current operational budget",
    },

    "budget_credibility_ratio": {
        "label": "Budget Credibility Ratio",
        "description": "Likelihood of budget being modified during the financial year",
        "interpretation": """A 100 percent ratio indicates that during the previous year's 
        budget was not changed altered suggesting that we shouldn't expect this year's 
        to change either."""
    },

    "cagr": {
        "label": "Compound Annual Growth Rate",
        "description": "The smoothed average annual growth rate of your budget over the past 2 years",
        "interpretation": """A high CAGR suggests that the budget has significantly changed 
        over the past 2 years""",
    },

    "personnel_cost_independent_agencies":{
        "label": "Personnel Cost for Independent Agencies",
        "description": """In the budget independent agencies will simply receive an allocation
        from the government and it is their responsibility on how that budget is spent""",
        "interpretation": """You will only see non-zero dollar amounts in the 
        transfers and subventions category"""
    }
}


def get_tooltip(field: str) -> str:
    meta = FIELD_METADATA.get(field)

    if not meta:
        return "No institutional definition available."

    return f"{meta['description']} {meta['interpretation']}"