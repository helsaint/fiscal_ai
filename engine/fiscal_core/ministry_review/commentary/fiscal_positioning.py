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
    }
}


def get_tooltip(field: str) -> str:
    meta = FIELD_METADATA.get(field)

    if not meta:
        return "No institutional definition available."

    return f"{meta['description']} {meta['interpretation']}"