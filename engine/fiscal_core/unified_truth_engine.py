import pandas as pd

from .scoring_engine import ScoringEngine
from .risk_engine import RiskEngine
from .efficiency_engine import EfficiencyEngine
from .benchmark_engine import BenchmarkEngine


class UnifiedTruthEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.master_df = master_df.copy()

        # Initialize component engines
        self.scoring_engine = ScoringEngine(self.master_df)
        self.risk_engine = RiskEngine(self.master_df)
        self.efficiency_engine = EfficiencyEngine(self.master_df)
        self.benchmark_engine = BenchmarkEngine(self.master_df)

    # ---------------------------------------------------
    # 1. Master Unified Table
    # ---------------------------------------------------

    def build_unified_table(self):
        """
        Produces one consolidated fiscal intelligence table.
        """

        # Unified scoring
        scored_df = self.scoring_engine.compute_unified_score()

        # Merge back into master for full context
        unified_df = self.master_df.merge(
            scored_df[['ministry', 'unified_score', 'unified_rank', 'unified_label']],
            on='ministry',
            how='left'
        )

        return unified_df.sort_values(by='unified_score', ascending=False)

    # ---------------------------------------------------
    # 2. Cabinet Critical List
    # ---------------------------------------------------

    def cabinet_critical_entities(self):
        scored_df = self.scoring_engine.compute_unified_score()
        return scored_df[scored_df['unified_label'] == 'Critical'] \
            .sort_values(by='unified_score', ascending=False)

    # ---------------------------------------------------
    # 3. Structural Distortion List
    # ---------------------------------------------------

    def structural_distortions(self):
        """
        High spend + low efficiency OR weak outcomes.
        """
        df = self.master_df[
            (self.master_df['very_high_spend'] == True) &
            (
                (self.master_df['low_efficiency'] == True) |
                (self.master_df['weak_outcomes'] == True)
            )
        ]

        return df[['ministry',
                   'total_spend_2026',
                   'efficiency_proxy',
                   'fiscal_risk_score']].sort_values(
            by='total_spend_2026', ascending=False
        )

    # ---------------------------------------------------
    # 4. High Value Entities
    # ---------------------------------------------------

    def high_value_entities(self):
        return self.efficiency_engine.high_value_ministries()

    # ---------------------------------------------------
    # 5. Escalation Watchlist
    # ---------------------------------------------------

    def escalation_watchlist(self):
        return self.risk_engine.escalation_watchlist()

    # ---------------------------------------------------
    # 6. Executive Snapshot
    # ---------------------------------------------------

    def executive_snapshot(self):
        scored_df = self.scoring_engine.compute_unified_score()

        return {
            "total_spend_2026": float(self.master_df['total_spend_2026'].sum()),
            "critical_entities": int((scored_df['unified_label'] == 'Critical').sum()),
            "elevated_entities": int((scored_df['unified_label'] == 'Elevated').sum()),
            "budget_pressure_entities": int(self.master_df['budget_pressure_flag'].sum()),
            "foreign_dependent_entities": int(self.master_df['foreign_dependent'].sum())
        }