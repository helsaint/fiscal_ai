from engine.ministry_efficiency_engine import MinistryEfficiencyEngine
from engine.loader import FiscalDataLoader


class FiscalAgent:
    def __init__(self):
        self.ministry_fiscal_summary_df = FiscalDataLoader().load_ministry_summary()
        self.eff_engine = MinistryEfficiencyEngine(
            self.ministry_fiscal_summary_df.ministry_summary
            )
        print(self.eff_engine.generate_summary())
