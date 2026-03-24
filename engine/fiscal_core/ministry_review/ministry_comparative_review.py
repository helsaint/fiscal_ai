# engine/comparative_engine.py

import numpy as np


def build_comparative_insight(df, ministry_row):

    ministry = ministry_row["ministry"]

    # Group by high spend ministries
    peers = df[df["spend_percentile"] >= 75]

    if len(peers) < 5:
        peers = df  # fallback if dataset small

    # Ranks
    efficiency_rank = ministry_row["efficiency_rank"]
    efficiency_percentile = (len(df) - efficiency_rank) / len(df) * 100

    peer_efficiency_rank = (
        peers["efficiency_rank"]
        .rank(method="min")
        .loc[ministry_row.name]
        if ministry_row.name in peers.index
        else None
    )

    # Efficiency flags
    is_low_efficiency = ministry_row["low_efficiency"]
    is_high_spend = ministry_row["high_spend"]

    # Comparative statements
    insights = []

    # 1. Overall positioning
    if efficiency_percentile < 40:
        insights.append("Ranks in the lower tier of ministries on efficiency")
    elif efficiency_percentile > 70:
        insights.append("Ranks among the stronger ministries on efficiency")

    # 2. Peer comparison
    if is_high_spend and is_low_efficiency:
        insights.append("Underperforms relative to other high-spend ministries")

    # 3. Outlier condition
    if ministry_row["high_spend_low_outcome"]:
        insights.append("Outlier: high expenditure with weak outcome delivery")

    return insights