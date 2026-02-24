import pandas as pd
from engine.fiscal_core.unified_truth_engine import UnifiedTruthEngine
from engine.fiscal_core.briefing_engine import BriefingEngine
from openai import OpenAI


class ExpenditureReviewAgent:
    def __init__(self, master_df: pd.DataFrame, openai_api_key: str):
        self.master_df = master_df
        self.truth_engine = UnifiedTruthEngine(master_df)
        self.briefing_engine = BriefingEngine(master_df)
        self.client = OpenAI(api_key=openai_api_key)

        # Structured state
        self.session_state = {
            "current_ministry": None,
            "last_brief": None,
            "last_risk_profile": None
        }

        # Conversational memory
        self.memory = []

    # ---------------------------------------------
    # Start or Switch Ministry Review
    # ---------------------------------------------

    def start_review(self, ministry_name: str):

        brief = self.briefing_engine.build_ministry_brief(ministry_name)

        if "error" in brief:
            return brief

        self.session_state["current_ministry"] = ministry_name
        self.session_state["last_brief"] = brief
        self.session_state["last_risk_profile"] = {
            "risk_label": brief["risk_label"],
            "supporting_flags": brief["supporting_flags"],
            "total_spend_2026": brief["total_spend_2026"]
        }

        # Reset conversational memory for new ministry
        self.memory = []

        return f"Review session started for {ministry_name}."

    # ---------------------------------------------
    # Conversational Follow-Up
    # ---------------------------------------------

    def ask(self, user_prompt: str):

        if not self.session_state["current_ministry"]:
            return "No ministry under review. Call start_review(ministry_name) first."

        context_block = f"""
        Current Ministry: {self.session_state['current_ministry']}

        Fiscal Profile:
        {self.session_state['last_risk_profile']}
        """

        full_prompt = context_block + "\nUser Question:\n" + user_prompt

        self.memory.append({"role": "user", "content": full_prompt})

        # Keep memory trimmed (last 8 exchanges)
        self.memory = self.memory[-8:]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.memory,
            temperature=0.2
        )

        assistant_reply = response.choices[0].message.content

        self.memory.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

    # ---------------------------------------------
    # Reset Session
    # ---------------------------------------------

    def reset_session(self):
        self.session_state = {
            "current_ministry": None,
            "last_brief": None,
            "last_risk_profile": None
        }
        self.memory = []