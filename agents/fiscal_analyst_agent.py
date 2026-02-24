import pandas as pd
from engine.fiscal_core.unified_truth_engine import UnifiedTruthEngine
from engine.fiscal_core.briefing_engine import BriefingEngine
from openai import OpenAI


class FiscalAnalystAgent:
    def __init__(self, master_df: pd.DataFrame, openai_api_key: str):
        self.master_df = master_df
        self.truth_engine = UnifiedTruthEngine(master_df)
        self.briefing_engine = BriefingEngine(master_df)
        self.client = OpenAI(api_key=openai_api_key)

    # ---------------------------------------------------
    # 1. Get Critical Entities
    # ---------------------------------------------------

    def get_critical_entities(self):
        return self.truth_engine.cabinet_critical_entities()

    # ---------------------------------------------------
    # 2. Explain Ministry (LLM Narrative Layer)
    # ---------------------------------------------------

    def explain_ministry(self, ministry_name: str):
        brief = self.briefing_engine.build_ministry_brief(ministry_name)

        if "error" in brief:
            return brief

        prompt = f"""
        You are a senior Ministry of Finance fiscal analyst.

        Based on this structured fiscal intelligence:

        {brief}

        Provide a concise analytical explanation (not political language).
        Focus on fiscal risk, performance, and structural issues.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content

    # ---------------------------------------------------
    # 3. Executive Snapshot (Structured)
    # ---------------------------------------------------

    def executive_snapshot(self):
        return self.truth_engine.executive_snapshot()

    # ---------------------------------------------------
    # 4. Structural Distortions
    # ---------------------------------------------------

    def structural_distortions(self):
        return self.truth_engine.structural_distortions()