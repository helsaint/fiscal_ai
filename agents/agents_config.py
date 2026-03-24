FISCAL_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "analysis": {"type": "string"},
        "key_risk_driver": {"type": "string"},
        "oversight_priority": {"type": "string"},
        "recommended_action": {"type": "string"}
    },
    "required": [
        "analysis",
        "key_risk_driver",
        "oversight_priority",
        "recommended_action"
    ],
    "additionalProperties": False
}

EXPENDITURE_REVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "review_rationale": {"type": "string"},
        "priority_review_area": {"type": "string"},
        "efficiency_opportunity": {"type": "string"},
        "recommended_review_action": {"type": "string"}
    },
    "required": [
        "review_rationale",
        "priority_review_area",
        "efficiency_opportunity",
        "recommended_review_action"
    ],
    "additionalProperties": False
}

CABINET_BRIEFING_SCHEMA = {
    "type": "object",
    "properties": {
        "situation_summary": {"type": "string"},
        "key_issue": {"type": "string"},
        "fiscal_implication": {"type": "string"},
        "recommended_action": {"type": "string"}
    },
    "required": [
        "situation_summary",
        "key_issue",
        "fiscal_implication",
        "recommended_action"
    ],
    "additionalProperties": False
}