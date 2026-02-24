import pandas as pd

class MinistryEfficiencyEngine:

    def __init__(self, fiscal_df: pd.DataFrame):
        df = fiscal_df.copy()
        df = df[df["indicator_outcome_count"] > 0]
        df_outcome_deficient = fiscal_df.copy()
        df_outcome_deficient = df_outcome_deficient[
            (
                df_outcome_deficient['indicator_count'] > 0
                ) &
            (
                df_outcome_deficient['indicator_outcome_count'] == 0
             )
        ]
        self.df = df
        self.df_outcome_deficient = df_outcome_deficient

    def top_efficient(self, n=5):
        df = self.df.sort_values("efficiency_rank", ascending=True)
        return df[["ministry", "efficiency_rank", "spend_per_outcome", "total_spend_2026"]].head(n)

    def least_efficient(self, n=5):
        df = self.df.sort_values("efficiency_rank", ascending=False)
        return df[["ministry", "efficiency_rank", "spend_per_outcome", "total_spend_2026"]].head(n)

    def high_risk_ministries(self):
        df = self.df[self.df["high_spend_low_outcome"] == True]
        return df[["ministry", "total_spend_2026", "spend_per_outcome", "indicator_count"]]

    def foreign_dependency_risk(self):
        df = self.df[self.df["foreign_dependent"] == True]
        return df[["ministry", "foreign_dependency", "total_spend_2026"]]

    def capex_heavy_ministries(self):
        df = self.df[self.df["capex_heavy"] == True]
        return df[["ministry", "capex_ratio_budget_2026", "total_spend_2026"]]

    def outcome_deficient_agencies(self):
        df = self.df_outcome_deficient.copy()
        if df.empty:
            return None
        return df[["ministry", "total_spend_2026", 
                   "indicator_output_count", "indicator_outcome_count"]]
    
    def generate_summary(self) -> str:
        worst = self.least_efficient(5)
        best = self.top_efficient(5)
        high_risk = self.high_risk_ministries()
        deficient = self.outcome_deficient_agencies()

        text = "\nFISCAL EFFICIENCY SUMMARY (2026)\n"

        text += "\nHigh Concern Agencies/Ministries:\n"
        for _, r in worst.iterrows():
            text += f"- {r['ministry']} | Rank: {r['efficiency_rank']} | Spend per outcome: {round(r['spend_per_outcome'],2)}\n"

        text += "\nMost Efficient Agencies/Ministries:\n"
        for _, r in best.iterrows():
            text += f"- {r['ministry']} | Rank: {r['efficiency_rank']} | Spend per outcome: {round(r['spend_per_outcome'],2)}\n"

        if len(high_risk) > 0:
            text += "\nHigh Spend + Weak Outcome Flags:\n"
            for _, r in high_risk.iterrows():
                text += f"- {r['ministry']} | Spend: {round(r['total_spend_2026'],2)}\n"

        if deficient is not None:
            text +="\nAgencies reporting outputs but no measurable outcomes:\n"
            for _, r in deficient.iterrows():
                text += f"- {r['ministry']} | Spend: {round(r['total_spend_2026'],2)} | Outcomes: {r['indicator_outcome_count']} | Outputs: {r['indicator_output_count']}\n"
        else:
            text += "\nNo outcome-deficient entities detected.\n"

        return text
