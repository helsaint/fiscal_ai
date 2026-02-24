import pandas as pd


class EfficiencyEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.df = master_df.copy()
        self._prepare()

    def _prepare(self):
        self.performance_df = self.df[self.df['ministry'] != 'public debt']

    # ---------------------------------------------------
    # 1. Most Expensive Outcomes (Value Distortion)
    # ---------------------------------------------------

    def highest_cost_per_outcome(self, top_n=10):
        df = self.performance_df[
            self.performance_df['indicator_outcome_count'] > 0
        ].sort_values(by='spend_per_outcome', ascending=False)

        return df[['ministry',
                   'spend_per_outcome',
                   'total_spend_2026',
                   'efficiency_rank']].head(top_n)

    # ---------------------------------------------------
    # 2. Hidden Inefficiency
    # High spend + weak outcomes
    # ---------------------------------------------------

    def hidden_inefficiency(self):
        df = self.performance_df[
            (self.performance_df['very_high_spend'] == True) &
            (self.performance_df['weak_outcomes'] == True)
        ]

        return df[['ministry',
                   'total_spend_2026',
                   'spend_per_outcome',
                   'efficiency_rank',
                   'efficiency_proxy']].sort_values(
            by='total_spend_2026', ascending=False
        )

    # ---------------------------------------------------
    # 3. Strong Value Ministries
    # Low spend + strong outcomes
    # ---------------------------------------------------

    def high_value_ministries(self):
        df = self.performance_df[
            (self.performance_df['strong_outcomes'] == True) &
            (self.performance_df['low_spend'] == True)
        ]

        return df[['ministry',
                   'total_spend_2026',
                   'spend_per_outcome',
                   'efficiency_rank']].sort_values(
            by='efficiency_rank', ascending=True
        )

    # ---------------------------------------------------
    # 4. Fake Performance Detection
    # High efficiency rank but low outcome strength
    # ---------------------------------------------------

    def fake_performance(self):
        df = self.performance_df[
            (self.performance_df['high_efficiency'] == True) &
            (self.performance_df['indicator_outcome_strength'] < 0.3)
        ]

        return df[['ministry',
                   'efficiency_rank',
                   'indicator_outcome_strength',
                   'spend_per_outcome',
                   'total_spend_2026']].sort_values(
            by='indicator_outcome_strength'
        )

    # ---------------------------------------------------
    # 5. Efficiency Distribution Summary
    # ---------------------------------------------------

    def efficiency_summary(self):
        return {
            "avg_efficiency_proxy": float(self.performance_df['efficiency_proxy'].mean()),
            "median_spend_per_outcome": float(self.performance_df['spend_per_outcome'].median()),
            "low_efficiency_count": int(self.performance_df['low_efficiency'].sum()),
            "high_efficiency_count": int(self.performance_df['high_efficiency'].sum())
        }
