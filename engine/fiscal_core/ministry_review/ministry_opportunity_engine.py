import numpy as np


def __compute_efficiency_gap(df, ministry_row):

    # Benchmarks
    median_efficiency = df["efficiency_rank"].median()
    top_quartile = np.percentile(df["efficiency_rank"], 25)

    current_efficiency = ministry_row["efficiency_rank"]

    return {
        "median_gap": current_efficiency - median_efficiency,
        "top_quartile_gap": current_efficiency - top_quartile
    }


def estimate_savings_proxy(df, ministry_row):

    total_spend = ministry_row["total_spend_2026"]

    gaps = __compute_efficiency_gap(df, ministry_row)

    # Normalize to avoid negative values
    median_gap = max(gaps["median_gap"], 0)
    top_gap = max(gaps["top_quartile_gap"], 0)

    # Scale factor
    scaling_factor = 0.01

    median_savings = total_spend * median_gap * scaling_factor
    top_savings = total_spend * top_gap * scaling_factor

    return {
        "median_savings": median_savings,
        "top_quartile_savings": top_savings
    }

# Build narrative text
def build_opportunity_statement(df, ministry_row):

    savings = estimate_savings_proxy(df, ministry_row)

    median = savings["median_savings"]
    top = savings["top_quartile_savings"]

    if median <= 0:
        return "Efficiency performance is broadly aligned with system benchmarks"

    if median > 0 and median < 1e6:
        return "Limited fiscal efficiency gains available under current structure"

    if median >= 1e6 and median < 1e8:
        return "Moderate fiscal space could be unlocked through efficiency improvements"

    if median >= 1e8:
        return "Significant fiscal space could be unlocked through efficiency reforms"

    return ""