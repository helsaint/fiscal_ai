import pandas as pd

class FiscalEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.df = master_df.copy()
        self._prepare()

    def _prepare(self):
        # exclude public debt from performance logic
        self.performance_df = self.df[self.df['ministry'] != 'public debt']
        self.ministry_only_df = self.df[
            self.df['agency_type'] == 'ministry']

    # ---------------------------------------------------
    # CORE LISTS
    # ---------------------------------------------------

    def get_budget_pressure(self):
        df = self.df[self.df['budget_pressure_flag'] == True]
        return df[['ministry', 'total_spend_2026', 'fiscal_risk_score']]\
            .sort_values(by='total_spend_2026', ascending=False)

    def get_high_performers(self):
        df = self.performance_df[self.performance_df['high_performer_flag'] == True]
        return df[['ministry', 'efficiency_rank', 'spend_per_outcome']]\
            .sort_values(by='efficiency_rank', ascending=True)

    def get_low_efficiency(self, top_n=10):
        df = self.performance_df.sort_values(by='efficiency_rank', ascending=False)
        return df[['ministry', 'efficiency_rank', 'spend_per_outcome', 'total_spend_2026']].head(top_n)

    def get_high_efficiency(self, top_n=10):
        df = self.performance_df.sort_values(by='efficiency_rank', ascending=True)
        return df[['ministry', 'efficiency_rank', 'spend_per_outcome', 'total_spend_2026']].head(top_n)

    # ---------------------------------------------------
    # CONCERN DETECTION (CABINET VIEW)
    # ---------------------------------------------------

    def get_structural_concerns(self):
        """
        Ministries that:
        - spend a lot
        - weak outcomes OR low efficiency
        - NOT public debt
        """
        df = self.performance_df[
            (self.performance_df['very_high_spend'] == True) &
            (
                (self.performance_df['weak_outcomes'] == True) |
                (self.performance_df['low_efficiency'] == True)
            )
        ]

        return df[['ministry',
                   'total_spend_2026',
                   'spend_per_outcome',
                   'efficiency_rank',
                   'fiscal_risk_score']]\
            .sort_values(by='total_spend_2026', ascending=False)

    def get_outcome_gaps(self):
        """
        Ministries with outputs but weak outcomes
        """
        df = self.performance_df[
            (self.performance_df['indicator_output_count'] > 0) &
            (self.performance_df['indicator_outcome_count'] == 0)
        ]

        return df[['ministry',
                   'indicator_output_count',
                   'indicator_outcome_count',
                   'total_spend_2026']].sort_values(
            by='total_spend_2026', ascending=False
        )

    # ---------------------------------------------------
    # FISCAL RISK OVERVIEW
    # ---------------------------------------------------

    def fiscal_risk_table(self):
        return self.df[['ministry',
                        'fiscal_risk_score',
                        'fiscal_risk_label',
                        'budget_pressure_flag',
                        'foreign_dependent',
                        'capex_pressure']]\
            .sort_values(by='fiscal_risk_score', ascending=False)

    # ---------------------------------------------------
    # CABINET SUMMARY SNAPSHOT
    # ---------------------------------------------------

    def cabinet_summary(self):
        total_spend = self.df['total_spend_2026'].sum()
        budget_pressure_count = self.df['budget_pressure_flag'].sum()
        high_performer_count = self.df['high_performer_flag'].sum()
        high_risk_count = (self.df['fiscal_risk_label'] == 'High').sum()

        return {
            "total_spend_2026": float(total_spend),
            "budget_pressure_entities": int(budget_pressure_count),
            "high_performers": int(high_performer_count),
            "high_fiscal_risk_entities": int(high_risk_count)
        }
