
# takes profile created build_ministry_profile()
# uses spend_percentile, foreing_risk, outcomes etc. to create useful NL summary
# for numerical values

def build_priority_signals(profile: dict) -> list:
    signals = []

    # Expenditure Concentration

    percentile = profile["spend_percentile"]
    percentile = round(percentile*100)
    if percentile >= 85:
        severity = "High"
        summary = f"Positioned in the {percentile}th expenditure percentile — systemically significant fiscal footprint."
    elif percentile >= 70:
        severity = "Moderate"
        summary = f"Positioned in the {percentile}th expenditure percentile — elevated fiscal scale."
    else:
        severity = "Contained"
        summary = f"Positioned in the {percentile}th expenditure percentile — standard fiscal scale."

    signals.append({
        "title": "Expenditure Concentration",
        "severity": severity,
        "summary": summary
    })

    # Capital Structure Pressure

    if profile["capex_pressure"] or profile["capex_risk"]:
        severity = "High"
        summary = "Capital expenditure structure indicates elevated execution or absorption pressure."
    else:
        severity = "Contained"
        summary = "Capital structure within normal peer-adjusted range."

    signals.append({
        "title": "Capital Structure Pressure",
        "severity": severity,
        "summary": summary
    })

    # Foreign Financing Risk

    if profile["foreign_risk"]:
        severity = "High"
        summary = f"{round(profile['foreign_dependency']*100,1)}% of capital expenditure externally financed — exposure to external funding volatility."
    elif profile["foreign_dependency"] > 0.2:
        severity = "Moderate"
        summary = f"{round(profile['foreign_dependency']*100,1)}% of capital expenditure externally financed."
    else:
        severity = "Contained"
        summary = "Limited reliance on external capital financing."

    signals.append({
        "title": "Foreign Financing Exposure",
        "severity": severity,
        "summary": summary
    })

    # Efficiency & outcome performance

    if profile["low_efficiency"] or profile["weak_outcomes"]:
        severity = "High"
        summary = f"Efficiency rank positioned at {profile['efficiency_rank']} with weak outcome indicators."
    elif profile["high_efficiency"]:
        severity = "Contained"
        summary = "Strong relative efficiency and outcome alignment."
    else:
        severity = "Moderate"
        summary = f"Efficiency rank positioned at {profile['efficiency_rank']} — mid-tier delivery performance."

    signals.append({
        "title": "Delivery & Outcome Performance",
        "severity": severity,
        "summary": summary
    })

    # Fiscal sustainability risk

    if profile["budget_pressure_flag"] or profile["fiscal_risk_score"] >= 75:
        severity = "High"
        summary = "Budget sustainability pressures identified within fiscal risk assessment."
    elif profile["fiscal_risk_score"] >= 55:
        severity = "Moderate"
        summary = "Moderate fiscal vulnerability requiring structured oversight."
    else:
        severity = "Contained"
        summary = "Fiscal sustainability position assessed as stable."

    signals.append({
        "title": "Fiscal Sustainability Risk",
        "severity": severity,
        "summary": summary
    })

    return signals