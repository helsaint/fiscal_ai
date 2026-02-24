import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "data"

class FiscalDataLoader:
    def __init__(self):
        self.revenue = None
        self.opex = None
        self.capex = None
        self.indicators = None
        self.ministry_summary = None

    def load_all(self):
        self.revenue = pd.read_csv(
            BASE_PATH / "budget_2026_volume_1_revenue_v2.csv"
            )
        self.opex = pd.read_csv(
            BASE_PATH / "BudgetCurrentExpenditure2026_v3.csv"
        )
        self.capex = pd.read_csv(
            BASE_PATH / "BudgetCapitalExpenditure_vol3_v4.csv"
        )
        self.indicators = pd.read_csv(
            BASE_PATH / "project_indicator_2026_v4.csv"
        )
        self.ministry_summary = pd.read_csv(
            BASE_PATH / "master_ministry_fiscal_intelligence.csv"
        )

        return self

    def load_ministry_summary(self):
        self.ministry_summary = pd.read_csv(
            BASE_PATH / "master_ministry_fiscal_intelligence.csv"
        )

        return self