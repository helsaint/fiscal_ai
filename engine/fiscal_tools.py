from engine.loader import FiscalDataLoader

class FiscalTools:

    def __init__(self):
        self.data = FiscalDataLoader().load_all()
        self.summary = self.data.ministry_summary

    # --------------------------------------------------
    # BASIC LOOKUPS
    # --------------------------------------------------

    def list_ministries(self):
        return sorted(self.summary["ministry"].unique().tolist())

    def get_ministry_summary(self, ministry: str):
        df = self.summary[self.summary["ministry"].str.lower() == ministry.lower()]
        if df.empty:
            return {"error": f"Ministry '{ministry}' not found"}
        return df.to_dict(orient="records")[0]

    # --------------------------------------------------
    # TOP SPENDING ANALYSIS
    # --------------------------------------------------

    def top_spending_ministries(self, n=10):
        df = self.summary.sort_values("total_spend_2026", ascending=False)
        return df.head(n)[["ministry", "total_spend_2026"]].to_dict(orient="records")

    def capex_heavy_ministries(self, threshold=0.4):
        df = self.summary[self.summary["capex_ratio_budget_2026"] > threshold]
        df = df.sort_values("capex_ratio_budget_2026", ascending=False)
        return df[["ministry", "capex_ratio_budget_2026"]].to_dict(orient="records")

    # --------------------------------------------------
    # EFFICIENCY + OUTCOME
    # --------------------------------------------------

    def low_outcome_ministries(self, threshold=0.4):
        df = self.summary[self.summary["indicator_outcome_ratio"] < threshold]
        df = df.sort_values("indicator_outcome_ratio")
        return df[
            ["ministry", "indicator_outcome_ratio", "total_spend_2026"]
        ].to_dict(orient="records")

    def high_spend_low_outcome(self):
        df = self.summary[self.summary["high_spend_low_outcome"] == True]
        return df[
            ["ministry", "total_spend_2026", "indicator_outcome_ratio"]
        ].to_dict(orient="records")

    def most_efficient_ministries(self, n=10):
        df = self.summary.sort_values("efficiency_rank")
        return df.head(n)[
            ["ministry", "efficiency_proxy", "total_spend_2026"]
        ].to_dict(orient="records")

    # --------------------------------------------------
    # FOREIGN DEPENDENCY
    # --------------------------------------------------

    def foreign_dependent_ministries(self, threshold=0.5):
        df = self.summary[self.summary["foreign_dependency"] > threshold]
        df = df.sort_values("foreign_dependency", ascending=False)

        return df[
            ["ministry", "foreign_dependency", "capex_2026"]
        ].to_dict(orient="records")

    # --------------------------------------------------
    # NATIONAL TOTALS
    # --------------------------------------------------

    def national_spending_summary(self):
        total_spend = self.summary["total_spend_2026"].sum()
        total_capex = self.summary["capex_2026"].sum()
        total_opex = self.summary["opex_2026"].sum()

        return {
            "total_spend_2026": float(total_spend),
            "total_capex_2026": float(total_capex),
            "total_opex_2026": float(total_opex),
            "capex_share": float(total_capex / total_spend),
            "opex_share": float(total_opex / total_spend),
        }
    # --------------------------------------------------
    # FISCAL EFFICIENCY TOOL
    # --------------------------------------------------
    def fiscal_efficiency(self):
        analysis_df = self.summary[self.summary['agency_type'] == 'ministry'].copy()
        final_cols = [
            "ministry",
            "total_spend_2026",
            "fiscal_risk_score",
            "fiscal_risk_label",
            "budget_pressure_flag",
            "performance_review_flag",
            "capex_pressure",
            "foreign_risk",
            "high_performer_flag",
            "indicator_outcome_count",
            "indicator_output_count",
            "spend_per_outcome",
            "efficiency_rank"
            ]
        fiscal_engine_output = analysis_df[final_cols].sort_values(
            "fiscal_risk_score", ascending=False
            )
