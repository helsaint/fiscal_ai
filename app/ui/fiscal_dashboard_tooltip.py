RISK_DRIVER_LABELS = {
    "efficiency_risk": "Efficiency Risk",
    "capex_risk": "Capital Execution Risk",
    "indicator_risk": "Indicator Coverage Risk",
    "foreign_risk": "Foreign Dependency Risk",
    "outcome_risk": "Outcome Delivery Risk"
}

def tooltip_classify_risk(score):
    
    if score >= 70:
        return '"Insolvency Danger." (The gov. are "one bad day" away from being broke)'
    elif score >= 50:
        return '"Structural Stress." (The gov. might need to borrow money soon).'
    elif score >= 30:
        return '"Yellow Flag." (Budget is tight, watch the edges).'
    else:
        return '"Fiscal Green Light." (Everything is covered).'
    
def tooltip_budget_pressure_percent(score):
    
    if score >= 70:
        return '"Governance Collapse." (The budget is no longer a functional document).'
    elif score >= 40:
        return '"Widespread Fragility." (The budget was likely based on unrealistic revenue goals).'
    elif score >= 16:
        return '"Selective Hardship." (Specific sectors struggling, but the rest are fine).'
    else:
        return '"Healthy Allocation."'
    
def _band_interpretation(metric_name, band):
    interpretations = {
        "Fiscal Risk": {
            "Stable": "Aggregate fiscal exposure remains within structural tolerance.",
            "Elevated": "System-wide fiscal exposure is moderately elevated.",
            "High": "Systemic fiscal vulnerability is forming.",
            "Critical": "Severe structural fiscal exposure detected."
        },
        "Outcome Risk": {
            "Stable": "Outcome delivery risk is contained.",
            "Elevated": "Performance conversion pressures are emerging.",
            "High": "Service delivery effectiveness is materially at risk.",
            "Critical": "System-wide outcome fragility requires urgent intervention."
        },
        "Budget Pressure": {
            "Stable": "Budgetary allocation pressure remains manageable.",
            "Elevated": "A material share of expenditure is under allocation stress.",
            "High": "Significant fiscal mass is experiencing budget strain.",
            "Critical": "Widespread allocation stress threatens operational continuity."
        }
    }

    return interpretations[metric_name][band]

def _fiscal_classify_band(value):
    if value < 0.4:
        return "Stable"
    elif value < 0.6:
        return "Elevated"
    elif value < 0.75:
        return "High"
    else:
        return "Critical"

def generate_graph_description(fr, orisk, bp):
    fr_band = _fiscal_classify_band(fr)
    or_band = _fiscal_classify_band(orisk)
    bp_band = _fiscal_classify_band(bp)

    description = f"""
    ### Fiscal Risk Landscape Overview

    This chart presents spend-weighted system-level risk intensities across three structural dimensions.

    - **Fiscal Risk ({fr:.2f}) — {fr_band}:**  
      {_band_interpretation("Fiscal Risk", fr_band)}

    - **Outcome Risk ({orisk:.2f}) — {or_band}:**  
      {_band_interpretation("Outcome Risk", or_band)}

    - **Budget Pressure ({bp:.2f}) — {bp_band}:**  
      {_band_interpretation("Budget Pressure", bp_band)}
    """

    # System-level synthesis logic
    if fr >= 0.6 and orisk >= 0.6:
        description += "\n\nOverall conditions indicate systemic fiscal and performance vulnerability requiring executive oversight."
    elif fr >= 0.4 or orisk >= 0.4:
        description += "\n\nStructural performance pressures are present but remain within reform-manageable bounds."
    else:
        description += "\n\nThe fiscal system is operating within stable structural parameters."

    return description

def _driver_band_meaning(band):
    meanings = {
        "Stable": "Exposure remains within structural tolerance.",
        "Elevated": "Moderate structural pressure detected.",
        "High": "Material vulnerability forming within this dimension.",
        "Critical": "Severe systemic fragility present in this dimension."
    }
    return meanings[band]

def generate_driver_narrative(driver_dict):
    """
    driver_dict example:
    {
        "efficiency_risk": 0.68,
        "capex_risk": 0.42,
        ...
    }
    """

    narrative = """
    The chart presents spend-weighted system-level intensities across core fiscal 
    vulnerability dimensions.
    """

    highest_driver = max(driver_dict, key=driver_dict.get)
    highest_value = driver_dict[highest_driver]

    for key, value in driver_dict.items():
        band = _fiscal_classify_band(value)
        label = RISK_DRIVER_LABELS[key]

        narrative += f"""
        - **{label} ({value:.2f}) — {band}:**  
        {_driver_band_meaning(band)}
        """

    # Executive synthesis
    highest_band = _fiscal_classify_band(highest_value)
    highest_label = RISK_DRIVER_LABELS[highest_driver]

    narrative += f"""
    **Dominant Structural Driver:** {highest_label} ({highest_band})
    """

    if highest_value >= 0.75:
        narrative += "System conditions indicate severe structural exposure requiring cabinet-level intervention."
    elif highest_value >= 0.6:
        narrative += "Material vulnerability detected; executive oversight recommended."
    elif highest_value >= 0.4:
        narrative += "Emerging pressure identified within system architecture."
    else:
        narrative += "Risk drivers remain within manageable institutional thresholds."

    return narrative