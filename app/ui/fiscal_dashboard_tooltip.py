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