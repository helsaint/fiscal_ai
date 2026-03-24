# We take the fiscal_ris_score and spend_percentile and
# create a textual interpretation so that users can
# easily interpret them

def generate_executive_headline(profile: dict):

    risk_score = profile["fiscal_risk_score"]
    spend_percentile = profile["spend_percentile"]

    # Create risk tiers.

    if risk_score >= 75:
        risk_tier = "high"
    elif risk_score >= 55:
        risk_tier = "moderate"
    else:
        risk_tier = "low"

    # Create spend scale tier

    if profile["very_high_spend"] or spend_percentile >= 85:
        scale_tier = "systemic"
    elif profile["high_spend"] or spend_percentile >= 70:
        scale_tier = "high"
    else:
        scale_tier = "standard"

    # Create a more useful synonym

    if profile["low_efficiency"]:
        efficiency_tier = "weak"
    elif profile["high_efficiency"]:
        efficiency_tier = "strong"
    else:
        efficiency_tier = "neutral"

    # Use combination of tiers to create text interpretation
    # This is also useful for the LLMs

    if (
        (risk_tier == "high" and scale_tier in ["systemic", "high"])
        or (risk_tier == "high" and efficiency_tier == "weak")
    ):
        posture = "High Intervention Priority"
        headline = "Systemically Exposed Ministry Requiring Immediate Fiscal Stabilisation"

    elif risk_tier == "moderate" and scale_tier in ["systemic", "high"]:
        posture = "Active Oversight Required"
        headline = "High-Exposure Ministry Requiring Tight Fiscal Control"

    elif risk_tier == "high":
        posture = "Active Risk Containment"
        headline = "Elevated Fiscal Risk Ministry Requiring Structured Risk Mitigation"

    elif risk_tier == "low" and efficiency_tier == "strong":
        posture = "Routine Executive Confidence"
        headline = "Operationally Stable Ministry with Strong Delivery Position"

    else:
        posture = "Targeted Monitoring"
        headline = "Moderate Fiscal Position Requiring Focused Oversight"

    # Create Priority Signals

    signals = []

    if scale_tier == "systemic":
        signals.append("Systemically Significant Expenditure Footprint")

    if profile["capex_pressure"]:
        signals.append("Elevated Capital Expenditure Pressure")

    if profile["foreign_risk"]:
        signals.append("Foreign Financing Dependency Risk")

    if efficiency_tier == "weak":
        signals.append("Below-Median Efficiency Performance")

    if profile["weak_outcomes"]:
        signals.append("Weak Outcome Indicator Strength")

    if profile["budget_pressure_flag"]:
        signals.append("Emerging Budget Sustainability Pressure")

    signals = signals[:5]

    return {
        "headline": headline,
        "posture": posture,
        "risk_score": risk_score,
        "risk_label": profile["fiscal_risk_label"],
        "spend_percentile": spend_percentile,
        "efficiency_rank": profile["efficiency_rank"],
        "signals": signals
    }