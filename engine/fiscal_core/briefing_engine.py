import pandas as pd


class BriefingEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.df = master_df.copy()
        self._prepare()

    def _prepare(self):
        self.df['ministry'] = self.df['ministry'].str.lower().str.strip()

    # ---------------------------------------------------
    # 1. Build Briefing Object for One Ministry
    # ---------------------------------------------------

    def build_ministry_brief(self, ministry_name: str):

        row = self.df[self.df['ministry'] == ministry_name.lower()]

        if row.empty:
            return {"error": "Ministry not found"}

        row = row.iloc[0]

        flags = []

        if row['budget_pressure_flag']:
            flags.append("budget pressure")

        if row['very_high_spend']:
            flags.append("very high spend")

        if row['low_efficiency']:
            flags.append("low efficiency")

        if row['weak_outcomes']:
            flags.append("weak outcomes")

        if row['foreign_dependent']:
            flags.append("foreign dependent")

        if row['capex_pressure']:
            flags.append("capex pressure")

        if row['performance_review_flag']:
            flags.append("performance review required")

        # Determine primary issue
        if row['fiscal_risk_label'] == 'High':
            primary_issue = "High fiscal risk exposure"
        elif row['low_efficiency'] and row['very_high_spend']:
            primary_issue = "High spend with weak efficiency"
        elif row['weak_outcomes']:
            primary_issue = "Weak outcome framework"
        else:
            primary_issue = "No critical structural issue"

        # Suggested Cabinet action logic
        if row['fiscal_risk_label'] == 'High':
            action = "Escalate to Cabinet review"
        elif row['performance_review_flag']:
            action = "Initiate performance review"
        elif row['low_efficiency']:
            action = "Request efficiency improvement plan"
        else:
            action = "Monitor"

        return {
            "ministry": row['ministry'],
            "total_spend_2026": float(row['total_spend_2026']),
            "fiscal_risk_score": float(row['fiscal_risk_score']),
            "risk_label": row['fiscal_risk_label'],
            "primary_issue": primary_issue,
            "supporting_flags": flags,
            "cabinet_action": action
        }

    # ---------------------------------------------------
    # 2. Build All High Risk Briefings
    # ---------------------------------------------------

    def build_high_risk_briefs(self):
        high_risk_df = self.df[self.df['fiscal_risk_label'] == 'High']
        briefs = []

        for ministry in high_risk_df['ministry']:
            briefs.append(self.build_ministry_brief(ministry))

        return briefs

    # ---------------------------------------------------
    # 3. Budget Pressure Briefings
    # ---------------------------------------------------

    def build_budget_pressure_briefs(self):
        pressure_df = self.df[self.df['budget_pressure_flag'] == True]
        briefs = []

        for ministry in pressure_df['ministry']:
            briefs.append(self.build_ministry_brief(ministry))

        return briefs

    # ---------------------------------------------------
    # 4. Top Critical (From Unified Score)
    # ---------------------------------------------------

    def build_critical_briefs(self, scored_df):
        critical_df = scored_df[scored_df['unified_label'] == 'Critical']
        briefs = []

        for ministry in critical_df['ministry']:
            briefs.append(self.build_ministry_brief(ministry))

        return briefs