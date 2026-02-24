import pandas as pd
import numpy as np


class BenchmarkEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.df = master_df.copy()
        self._prepare()

    def _prepare(self):
        self.df['ministry'] = self.df['ministry'].str.lower().str.strip()

        # Compute percentiles for benchmarking
        self.df['efficiency_percentile'] = self.df['efficiency_proxy'].rank(pct=True)
        self.df['outcome_strength_percentile'] = self.df['indicator_outcome_strength'].rank(pct=True)
        self.df['risk_percentile'] = self.df['fiscal_risk_score'].rank(pct=True)
        self.df['capex_intensity_percentile'] = self.df['capex_ratio_budget_2026'].rank(pct=True)

    # ---------------------------------------------------
    # 1. Benchmark by Agency Type
    # ---------------------------------------------------

    def peer_benchmark(self, agency_type_value):
        df = self.df[self.df['agency_type'] == agency_type_value]

        return df[['ministry',
                   'total_spend_2026',
                   'efficiency_percentile',
                   'outcome_strength_percentile',
                   'risk_percentile']].sort_values(
            by='risk_percentile', ascending=False
        )

    # ---------------------------------------------------
    # 2. Spend Outliers (Top 10%)
    # ---------------------------------------------------

    def spend_outliers(self):
        df = self.df[self.df['spend_percentile'] >= 0.90]

        return df[['ministry',
                   'total_spend_2026',
                   'spend_percentile',
                   'risk_percentile']].sort_values(
            by='total_spend_2026', ascending=False
        )

    # ---------------------------------------------------
    # 3. Efficiency Outliers (Bottom 10%)
    # ---------------------------------------------------

    def low_efficiency_outliers(self):
        df = self.df[self.df['efficiency_percentile'] <= 0.10]

        return df[['ministry',
                   'efficiency_proxy',
                   'efficiency_percentile',
                   'total_spend_2026']].sort_values(
            by='efficiency_percentile'
        )

    # ---------------------------------------------------
    # 4. High Risk Within Peer Group
    # ---------------------------------------------------

    def high_risk_within_peers(self):
        results = []

        for agency_type in self.df['agency_type'].unique():
            subset = self.df[self.df['agency_type'] == agency_type]
            top_risk = subset.sort_values(
                by='fiscal_risk_score',
                ascending=False
            ).head(1)

            results.append(top_risk)

        return pd.concat(results)[[
            'ministry',
            'agency_type',
            'fiscal_risk_score',
            'total_spend_2026'
        ]]

    # ---------------------------------------------------
    # 5. Region vs Central Comparison
    # ---------------------------------------------------

    def region_vs_central_summary(self):
        grouped = self.df.groupby('agency_type').agg({
            'total_spend_2026': 'mean',
            'efficiency_proxy': 'mean',
            'fiscal_risk_score': 'mean'
        }).reset_index()

        return grouped.sort_values(by='fiscal_risk_score', ascending=False)