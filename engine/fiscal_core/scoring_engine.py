import pandas as pd
import numpy as np


class ScoringEngine:
    def __init__(self, master_df: pd.DataFrame):
        self.df = master_df.copy()
        self._prepare()

    def _prepare(self):
        self.df['ministry'] = self.df['ministry'].str.lower().str.strip()

        # Normalize core numeric fields
        self.df['norm_fiscal_risk'] = self._normalize(self.df['fiscal_risk_score'])
        self.df['norm_efficiency'] = self._normalize(self.df['efficiency_proxy'])
        self.df['indicator_outcome_strength_numeric'] = self.df['indicator_outcome_strength'].map(
            {
                'very weak': 0,
                'weak': 1,
                'moderate': 2,
                'strong': 3,
                'very strong': 4
            }
        )
        self.df['norm_outcome_strength'] = self._normalize(
            self.df['indicator_outcome_strength_numeric']
            )

    def _normalize(self, series):
        return (series - series.min()) / (series.max() - series.min() + 1e-9)

    # ---------------------------------------------------
    # Unified Fiscal Authority Score
    # ---------------------------------------------------

    def compute_unified_score(self):

        df = self.df.copy()

        # Penalty flags
        df['pressure_penalty'] = df['budget_pressure_flag'].astype(int) * 0.10
        df['foreign_penalty'] = df['foreign_dependent'].astype(int) * 0.05
        df['capex_penalty'] = df['capex_pressure'].astype(int) * 0.05

        # Public debt should not get efficiency/outcome weight
        performance_mask = df['ministry'] != 'public debt'
    
        df['performance_component'] = 0
        df['performance_component'] = (
            (df['norm_efficiency'] * 0.25) +
            (df['norm_outcome_strength'] * 0.15)
        )
        df.loc[~performance_mask, 'performance_component'] = 0

        # Core weighted score
        df['raw_score'] = (
            (df['norm_fiscal_risk'] * 0.40) +
            df['performance_component'] +
            df['pressure_penalty'] +
            df['foreign_penalty'] +
            df['capex_penalty']
        )

        # Scale to 0–100
        df['unified_score'] = self._normalize(df['raw_score']) * 100

        # Rank
        df['unified_rank'] = df['unified_score'].rank(ascending=False)

        # Labeling
        df['unified_label'] = pd.cut(
            df['unified_score'],
            bins=[-1, 25, 50, 75, 100],
            labels=['Low', 'Moderate', 'Elevated', 'Critical']
        )

        return df[['ministry',
                   'unified_score',
                   'unified_rank',
                   'unified_label',
                   'fiscal_risk_score',
                   'efficiency_proxy',
                   'budget_pressure_flag']]
    
    # ---------------------------------------------------
    # Top Critical Ministries
    # ---------------------------------------------------

    def critical_entities(self):
        df = self.compute_unified_score()
        return df[df['unified_label'] == 'Critical']\
            .sort_values(by='unified_score', ascending=False)