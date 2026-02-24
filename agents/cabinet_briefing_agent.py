import pandas as pd
from engine.fiscal_core.unified_truth_engine import UnifiedTruthEngine
from engine.fiscal_core.briefing_engine import BriefingEngine
from openai import OpenAI


class CabinetBriefingAgent:
    def __init__(self, master_df: pd.DataFrame, openai_api_key: str):
        self.master_df = master_df
        self.truth_engine = UnifiedTruthEngine(master_df)
        self.briefing_engine = BriefingEngine(master_df)
        self.client = OpenAI(api_key=openai_api_key)

    # ---------------------------------------------------
    # 1. Single Ministry Cabinet Memo
    # ---------------------------------------------------

    def generate_ministry_memo(self, ministry_name: str):

        brief = self.briefing_engine.build_ministry_brief(ministry_name)

        if "error" in brief:
            return brief

        prompt = f"""
        You are drafting a formal Cabinet briefing note
        for the Ministry of Finance.

        Based strictly on the structured fiscal intelligence below:

        {brief}

        Produce a concise Cabinet briefing note with:
        - Heading
        - Fiscal Exposure Summary
        - Risk Assessment
        - Key Structural Issues
        - Recommended Action

        Use formal policy tone.
        No speculation.
        No political commentary.
        Keep it under 400 words.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15
        )

        return response.choices[0].message.content

    # ---------------------------------------------------
    # 2. Cabinet Critical Brief Pack
    # ---------------------------------------------------

    def generate_critical_brief_pack(self):

        critical_df = self.truth_engine.cabinet_critical_entities()

        memos = []

        for ministry in critical_df['ministry']:
            memo = self.generate_ministry_memo(ministry)
            memos.append({
                "ministry": ministry,
                "memo": memo
            })

        return memos

    # ---------------------------------------------------
    # 3. Executive Fiscal Snapshot Memo
    # ---------------------------------------------------

    def generate_executive_snapshot_memo(self):

        snapshot = self.truth_engine.executive_snapshot()

        prompt = f"""
        Draft a Cabinet-level fiscal overview based on:

        {snapshot}

        Structure:
        - Total Fiscal Position
        - Risk Concentration
        - Budget Pressure Landscape
        - Strategic Observations
        - Immediate Priorities

        Formal tone.
        Clear and direct.
        Under 500 words.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.15
        )

        return response.choices[0].message.content