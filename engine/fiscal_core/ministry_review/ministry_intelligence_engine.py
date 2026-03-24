import pandas as pd

# df is dataset from the master_ministry_fiscal_intelligence.csv
# ministry is the ministry of interest from the drop down in 2_Ministry_Review
# Uses the data to create a profile for the ministry

def build_ministry_profile(df: pd.DataFrame, ministry: str) -> dict:
    row = df[df["ministry"] == ministry]

    if row.empty:
        raise ValueError(f"Ministry '{ministry}' not found.")

    row = row.iloc[0]

    profile = {
        # Core Identifiers
        "ministry": row["ministry"],

        # Structural Spend
        "total_spend": row["total_spend_2026"],
        "spend_percentile": row["spend_percentile"],
        "high_spend": row["high_spend"],
        "very_high_spend": row["very_high_spend"],

        # Efficiency
        "efficiency_rank": row["efficiency_rank"],
        "efficiency_proxy": row["efficiency_proxy"],
        "low_efficiency": row["low_efficiency"],
        "high_efficiency": row["high_efficiency"],

        # Risk Scores
        "fiscal_risk_score": row["fiscal_risk_score"],
        "fiscal_risk_label": row["fiscal_risk_label"],

        # Risk Components
        "outcome_risk": row["outcome_risk"],
        "efficiency_risk": row["efficiency_risk"],
        "capex_risk": row["capex_risk"],
        "foreign_risk": row["foreign_risk"],
        "foreign_risk_num": row["foreign_risk_num"],

        # Structural Flags
        "capex_pressure": row["capex_pressure"],
        "foreign_dependency": row["foreign_dependency"],
        "weak_outcomes": row["weak_outcomes"],
        "budget_pressure_flag": row["budget_pressure_flag"],
        "performance_review_flag": row["performance_review_flag"],
        "high_performer_flag": row["high_performer_flag"],
    }

    return profile