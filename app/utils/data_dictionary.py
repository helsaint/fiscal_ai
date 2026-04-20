from __future__ import annotations
from typing import Dict
from pydantic import BaseModel # Used for data validation
from app.utils.dictionary_column_names import *

# Buidling Blocks
class ColumnMeta(BaseModel):
    desicription: str
    unit: str = ""
    is_synthesized: bool = False
    formula: str = ""
    example: str = ""

class TableMeta(BaseModel):
    description: str
    grain: str # explains what a single row represents
    primary_keys: list[str] = []
    join_hints: list[str] = [] # how to join datasets
    columns: Dict[str, ColumnMeta]

# Table definitions
DATA_DICTIONARY: Dict[str, TableMeta] = {
    # fiscal summary
    "fiscal_summary":TableMeta(
        description=(
            """Ministry/Government Agency level summary for fiscal intelligence dataset.
            It contains summed financial allocations for capex and opex, funding source either
            government (local) or foreign. It also includes performance metrics. Counts number of
            programs and outcome and output indicators. It also includes indicator outcome ratios
            and indicator output ratios. It also contains proxies for efficiency and risks flags.
            """
        ),
        grain = "One row per government ministry/agency",
        primary_keys=["ministry"],
        join_hints=["joins to opex and capex on ministry"],
        columns={
            "ministry": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["ministry"],
                example="ministry of agriculture",
            ),
            "opex_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_2025"],
                unit="GYD",
                example="1319046000.0",
            ),
            "opex_2025": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "opex_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_2025": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_actual_pre_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_actual_pre_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_actual_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_actual_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_actual_2025": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_actual_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_budget_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_budget_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_actual_pre_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_actual_pre_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_actual_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_actual_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_actual_2025": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_actual_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_budget_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_budget_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_ratio_budget_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_ratio_budget_2026"],
                example="0.02317605866787491"
            ),
            "capex_ratio_budget_2025": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_ratio_budget_2025"],
                example="0.02317605866787491"
            ),
            "capex_ratio_budget_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_ratio_budget_2024"],
                example="0.02317605866787491"
            ),
            "opex_ratio_budget_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_ratio_budget_2026"],
                example="0.02317605866787491"
            ),
            "opex_ratio_budget_2025": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_ratio_budget_2025"],
                example="0.02317605866787491"
            ),
            "opex_ratio_budget_2024": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_ratio_budget_2024"],
                example="0.02317605866787491"
            ),
            "programme_count": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["programme_count"],
                example="2"
            ),
            "indicator_outcome_count": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_outcome_count"],
                example="12.0"
            ),
            "indicator_output_count": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_output_count"],
                example="12.0"
            ),
            "agency_type": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["agency_type"],
                example="ministry"
            ),
            "indicator_outcome_ratio": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_outcome_ratio"],
                example="0.2"
            ),
            "indicator_output_ratio": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_output_ratio"],
                example="0.2"
            ),
            "sector_count": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["sector_count"],
                example="3.0"
            ),
            "spend_per_indicator": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_per_indicator"],
                unit="GYD",
                example="345183800.0",
            ),
            "spend_per_outcome": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_per_outcome"],
                unit="GYD",
                example="345183800.0",
            ),
            "capex_heavy": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_heavy"],
                example="False",
            ),
            "high_spend_low_outcome": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_spend_low_outcome"],
                example="False",
            ),
            "total_spend_2026": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["total_spend_2026"],
                unit="GYD",
                example="1725919000.0",
            ),
            "indicator_count": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_count"],
                example="5.0",
            ),
            "indicator_outcome_strength": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_outcome_strength"],
                example="very weak",
            ),
            "indicator_coverage": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_coverage"],
                example="very low",
            ),
            "spend_intensity": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_intensity"],
                example="very low",
            ),
            "efficiency_proxy": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["efficiency_proxy"],
                example="5.794014666968728e-10",
            ),
            "efficiency_rank": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["efficiency_rank"],
                example="22.0",
            ),
            "foreign_dependency": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_dependency"],
                example="0.0",
            ),
            "foreign_dependent": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_dependent"],
                example="False",
            ),
            "spend_percentile": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_percentile"],
                example="0.2391304347826087",
            ),
            "high_spend": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_spend"],
                example="False",
            ),
            "very_high_spend": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["very_high_spend"],
                example="False",
            ),
            "low_spend": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["low_spend"],
                example="False",
            ),
            "weak_outcomes": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["weak_outcomes"],
                example="False",
            ),
            "strong_outcomes": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["strong_outcomes"],
                example="False",
            ),
            "low_efficiency": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["low_efficiency"],
                example="False",
            ),
            "high_efficiency": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_efficiency"],
                example="False",
            ),
            "capex_pressure": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_pressure"],
                example="False",
            ),
            "foreign_risk": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_risk"],
                example="False",
            ),
            "budget_pressure_flag": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["budget_pressure_flag"],
                example="False",
            ),
            "performance_review_flag": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["performance_review_flag"],
                example="False",
            ),
            "high_performer_flag": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_performer_flag"],
                example="False",
            ),
            "outcome_risk": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["outcome_risk"],
                example="0.8",
            ),
            "capex_risk": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_risk"],
                example="0.5365853658536586",
            ),
            "foreign_risk_num": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_risk_num"],
                example="0.02317605866787491",
            ),
            "indicator_risk": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_risk"],
                example="0.02317605866787491",
            ),
            "fiscal_risk_score": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["fiscal_risk_score"],
                example="52.87815531969896",
            ),
            "fiscal_risk_label": ColumnMeta(
                desicription=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["fiscal_risk_label"],
                example="stable",
            ),
        }
    )
}

