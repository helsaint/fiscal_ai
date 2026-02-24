import pandas as pd


class RiskEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.df = master_df.copy()
        self._prepare()

    def _prepare(self):
        self.df['ministry'] = self.df['ministry'].str.lower().str.strip()

    # ---------------------------------------------------
    # 1. High Fiscal Risk Ministries
    # ---------------------------------------------------

    def high_fiscal_risk(self):
        df = self.df[self.df['fiscal_risk_label'] == 'High']

        return df[['ministry',
                   'fiscal_risk_score',
                   'total_spend_2026',
                   'budget_pressure_flag',
                   'foreign_dependent']].sort_values(
            by='fiscal_risk_score', ascending=False
        )

    # ---------------------------------------------------
    # 2. Budget Pressure Entities
    # ---------------------------------------------------

    def budget_pressure_entities(self):
        df = self.df[self.df['budget_pressure_flag'] == True]

        return df[['ministry',
                   'total_spend_2026',
                   'fiscal_risk_score',
                   'capex_pressure']].sort_values(
            by='total_spend_2026', ascending=False
        )

    # ---------------------------------------------------
    # 3. Structural Risk (Spending + Weak Delivery)
    # ---------------------------------------------------

    def structural_risk(self):
        df = self.df[
            (self.df['very_high_spend'] == True) &
            (
                (self.df['weak_outcomes'] == True) |
                (self.df['low_efficiency'] == True)
            )
        ]

        return df[['ministry',
                   'total_spend_2026',
                   'fiscal_risk_score',
                   'efficiency_risk',
                   'outcome_risk']].sort_values(
            by='total_spend_2026', ascending=False
        )

    # ---------------------------------------------------
    # 4. Foreign Exposure Risk
    # ---------------------------------------------------

    def foreign_dependency_risk(self):
        df = self.df[self.df['foreign_dependent'] == True]

        return df[['ministry',
                   'foreign_risk_num',
                   'total_spend_2026',
                   'capex_pressure']].sort_values(
            by='foreign_risk_num', ascending=False
        )

    # ---------------------------------------------------
    # 5. Escalation List (Cabinet Watchlist)
    # ---------------------------------------------------

    def escalation_watchlist(self):
        """
        Ministries that meet 2 or more major risk flags.
        """
        risk_flags = [
            'budget_pressure_flag',
            'performance_review_flag',
            'foreign_dependent',
            'capex_pressure'
        ]

        df = self.df.copy()
        df['risk_flag_count'] = df[risk_flags].sum(axis=1)

        watchlist = df[df['risk_flag_count'] >= 2]

        return watchlist[['ministry',
                          'risk_flag_count',
                          'fiscal_risk_score',
                          'total_spend_2026']].sort_values(
            by='risk_flag_count', ascending=False
        )

    # ---------------------------------------------------
    # 6. Risk Summary Snapshot
    # ---------------------------------------------------

    def risk_summary(self):
        return {
            "high_fiscal_risk_count": int((self.df['fiscal_risk_label'] == 'High').sum()),
            "budget_pressure_count": int(self.df['budget_pressure_flag'].sum()),
            "foreign_dependent_count": int(self.df['foreign_dependent'].sum()),
            "capex_pressure_count": int(self.df['capex_pressure'].sum()),
            "performance_review_count": int(self.df['performance_review_flag'].sum())
        }