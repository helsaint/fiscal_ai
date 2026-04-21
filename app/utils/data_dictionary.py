from __future__ import annotations
from typing import Dict
from pydantic import BaseModel # Used for data validation
from app.utils.dictionary_column_names import *

# Buidling Blocks
class ColumnMeta(BaseModel):
    description: str
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
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_2025"],
                unit="GYD",
                example="1319046000.0",
            ),
            "opex_2025": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "opex_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_2025": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_actual_pre_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_actual_pre_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_actual_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_actual_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_actual_2025": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_actual_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "foreign_capex_budget_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_capex_budget_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_actual_pre_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_actual_pre_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_actual_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_actual_2024"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_actual_2025": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_actual_2025"],
                unit="GYD",
                example="1319046000.0"
            ),
            "gov_capex_budget_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["gov_capex_budget_2026"],
                unit="GYD",
                example="1319046000.0"
            ),
            "capex_ratio_budget_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_ratio_budget_2026"],
                example="0.02317605866787491"
            ),
            "capex_ratio_budget_2025": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_ratio_budget_2025"],
                example="0.02317605866787491"
            ),
            "capex_ratio_budget_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_ratio_budget_2024"],
                example="0.02317605866787491"
            ),
            "opex_ratio_budget_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_ratio_budget_2026"],
                example="0.02317605866787491"
            ),
            "opex_ratio_budget_2025": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_ratio_budget_2025"],
                example="0.02317605866787491"
            ),
            "opex_ratio_budget_2024": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["opex_ratio_budget_2024"],
                example="0.02317605866787491"
            ),
            "programme_count": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["programme_count"],
                example="2"
            ),
            "indicator_outcome_count": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_outcome_count"],
                example="12.0"
            ),
            "indicator_output_count": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_output_count"],
                example="12.0"
            ),
            "agency_type": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["agency_type"],
                example="ministry"
            ),
            "indicator_outcome_ratio": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_outcome_ratio"],
                example="0.2"
            ),
            "indicator_output_ratio": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_output_ratio"],
                example="0.2"
            ),
            "sector_count": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["sector_count"],
                example="3.0"
            ),
            "spend_per_indicator": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_per_indicator"],
                unit="GYD",
                example="345183800.0",
            ),
            "spend_per_outcome": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_per_outcome"],
                unit="GYD",
                example="345183800.0",
            ),
            "capex_heavy": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_heavy"],
                example="False",
            ),
            "high_spend_low_outcome": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_spend_low_outcome"],
                example="False",
            ),
            "total_spend_2026": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["total_spend_2026"],
                unit="GYD",
                example="1725919000.0",
            ),
            "indicator_count": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_count"],
                example="5.0",
            ),
            "indicator_outcome_strength": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_outcome_strength"],
                example="very weak",
            ),
            "indicator_coverage": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_coverage"],
                example="very low",
            ),
            "spend_intensity": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_intensity"],
                example="very low",
            ),
            "efficiency_proxy": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["efficiency_proxy"],
                example="5.794014666968728e-10",
            ),
            "efficiency_rank": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["efficiency_rank"],
                example="22.0",
            ),
            "foreign_dependency": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_dependency"],
                example="0.0",
            ),
            "foreign_dependent": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_dependent"],
                example="False",
            ),
            "spend_percentile": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["spend_percentile"],
                example="0.2391304347826087",
            ),
            "high_spend": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_spend"],
                example="False",
            ),
            "very_high_spend": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["very_high_spend"],
                example="False",
            ),
            "low_spend": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["low_spend"],
                example="False",
            ),
            "weak_outcomes": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["weak_outcomes"],
                example="False",
            ),
            "strong_outcomes": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["strong_outcomes"],
                example="False",
            ),
            "low_efficiency": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["low_efficiency"],
                example="False",
            ),
            "high_efficiency": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_efficiency"],
                example="False",
            ),
            "capex_pressure": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_pressure"],
                example="False",
            ),
            "foreign_risk": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_risk"],
                example="False",
            ),
            "budget_pressure_flag": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["budget_pressure_flag"],
                example="False",
            ),
            "performance_review_flag": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["performance_review_flag"],
                example="False",
            ),
            "high_performer_flag": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["high_performer_flag"],
                example="False",
            ),
            "outcome_risk": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["outcome_risk"],
                example="0.8",
            ),
            "capex_risk": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["capex_risk"],
                example="0.5365853658536586",
            ),
            "foreign_risk_num": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["foreign_risk_num"],
                example="0.02317605866787491",
            ),
            "indicator_risk": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["indicator_risk"],
                example="0.02317605866787491",
            ),
            "fiscal_risk_score": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["fiscal_risk_score"],
                example="52.87815531969896",
            ),
            "fiscal_risk_label": ColumnMeta(
                description=MASTER_MINISTRY_FISCAL_INTELLIGENCE_DICTIONARY["fiscal_risk_label"],
                example="stable",
            ),
        }
    ),

    # opex
    "opex": TableMeta(
        description=(
            """ Provides opex spend for each ministry by the account code. It includes spend
            from the past two years as well as the current budgeted spend. It contains allocation 
            for opex for each ministry by each programme within that ministry. It includes 
            funding source either government or foreign funded. Other information included description 
            of expenditures.
            """),
        grain="one row represents expenditure by ministry/agency and the account code",
        primary_keys=["ministry", "account_code"],
        join_hints=["joins to capex on ministry and programme", "join to fiscal_summary on ministry but will have to first aggregate on the ministry"],
        columns={
            "description": ColumnMeta(
                description=OPEX_DICTIONARY["description"],
                example="6011 statutory wages and salaries",
            ),
            "actual_2024": ColumnMeta(
                description=OPEX_DICTIONARY["actual_2024"],
                unit="GYD",
                example="27820000.0",
            ),
            "budget_2025": ColumnMeta(
                description=OPEX_DICTIONARY["budget_2025"],
                unit="GYD",
                example="27820000.0",
            ),
            "revised_2025": ColumnMeta(
                description=OPEX_DICTIONARY["revised_2025"],
                unit="GYD",
                example="27820000.0",
            ),
            "budget_2026": ColumnMeta(
                description=OPEX_DICTIONARY["budget_2026"],
                unit="GYD",
                example="30046000.0",
            ),
            "agency": ColumnMeta(
                description=OPEX_DICTIONARY["agency"],
                example="01 office of the president",
            ),
            "programme": ColumnMeta(
                description=OPEX_DICTIONARY["programme"],
                example="011 - administration",
            ),
            "ministry": ColumnMeta(
                description=OPEX_DICTIONARY["ministry"],
                example="office of the president",
            ),
            "start_date": ColumnMeta(
                description=OPEX_DICTIONARY["start_date"],
                example="01-jan-2026",
            ),
            "end_date": ColumnMeta(
                description=OPEX_DICTIONARY["end_date"],
                example="31-dec-2026",
            ),
            "foreign_funding": ColumnMeta(
                description=OPEX_DICTIONARY["foreign_funding"],
                unit="GYD",
                example="0.0",
            ),
            "expenditure_type": ColumnMeta(
                description=OPEX_DICTIONARY["expenditure_type"],
                example="current",
            ),
            "government_funding": ColumnMeta(
                description=OPEX_DICTIONARY["government_funding"],
                unit="GYD",
                example="30046000.0",
            ),
            "cost": ColumnMeta(
                description=OPEX_DICTIONARY["cost"],
                unit="GYD",
                example="30046000.0",
            ),
            "account_code": ColumnMeta(
                description=OPEX_DICTIONARY["account_code"],
                example="6011",
            ),
            "account_description": ColumnMeta(
                description=OPEX_DICTIONARY["account_description"],
                example="statutory wages and salaries",
            ),
            "account_name": ColumnMeta(
                description=OPEX_DICTIONARY["account_name"],
                example="statutory wages and salaries",
            ),
            "economic_group": ColumnMeta(
                description=OPEX_DICTIONARY["economic_group"],
                example="Compensation of Employees",
            ),
            "economic_subgroup": ColumnMeta(
                description=OPEX_DICTIONARY["economic_subgroup"],
                example="Statutory Wages",
            ),
            "spending_type": ColumnMeta(
                description=OPEX_DICTIONARY["spending_type"],
                example="Personnel",
            ),
            "rigidity": ColumnMeta(
                description=OPEX_DICTIONARY["rigidity"],
                example="Rigid",
            ),
            "policy_area": ColumnMeta(
                description=OPEX_DICTIONARY["policy_area"],
                example="General Public Services",
            ),
            "tags": ColumnMeta(
                description=OPEX_DICTIONARY["tags"],
                example="wage_bill,statutory,personnel",
            ),
        }
    ),

    # capex
    "capex": TableMeta(
        description=(
            """
            Provides opex spend for each ministry by the programme and project name (title). 
            It includes spend from the past two years as well as the current budgeted spend. 
            It contains allocation for capex for each ministry by each programme and the project
            title. It includes funding source either government or foreign funded. Other information 
            included description of the project.
            """
        ),
        grain="One row describes the budget and current costs of project for each programme within each ministry",
        primary_keys=["programme", "ministry", "title"],
        join_hints=["join opex on ministry and programme but will have to aggregate on these two fields first", "join fiscal_summary on ministry but will first have to aggregate on ministry"],
        columns={
            "programme": ColumnMeta(
                description=CAPEX_DICTIONARY["programme"],
                example="011 - administration",
            ),
            "title": ColumnMeta(
                description=CAPEX_DICTIONARY["title"],
                example="gas to power project",
            ),
            "ministry": ColumnMeta(
                description=CAPEX_DICTIONARY["ministry"],
                example="office of the prime minister",
            ),
            "description": ColumnMeta(
                description=CAPEX_DICTIONARY["description"],
                example="the project entails provision for furniture and equipment.",
            ),
            "total_project_cost": ColumnMeta(
                description=CAPEX_DICTIONARY["total_project_cost"],
                unit="GYD",
                example="8750625000",
            ),
            "total_foreign_funding": ColumnMeta(
                description=CAPEX_DICTIONARY["total_foreign_funding"],
                unit="GYD",
                example="521250000",
            ),
            "total_government_funding": ColumnMeta(
                description=CAPEX_DICTIONARY["total_government_funding"],
                unit="GYD",
                example="150000000",
            ),
            "start_date": ColumnMeta(
                description=CAPEX_DICTIONARY["start_date"],
                example="01-Jan-24",
            ),
            "end_date": ColumnMeta(
                description=CAPEX_DICTIONARY["end_date"],
                example="31-Dec-31",
            ),
            "foreign_actual_pre_2024": ColumnMeta(
                description=CAPEX_DICTIONARY["foreign_actual_pre_2024"],
                unit="GYD",
                example="0",
            ),
            "foreign_actual_2024": ColumnMeta(
                description=CAPEX_DICTIONARY["foreign_actual_2024"],
                unit="GYD",
                example="0",
            ),
            "foreign_actual_2025": ColumnMeta(
                description=CAPEX_DICTIONARY["foreign_actual_2025"],
                unit="GYD",
                example="0",
            ),
            "foreign_actual_2026": ColumnMeta(
                description=CAPEX_DICTIONARY["foreign_actual_2026"],
                unit="GYD",
                example="2000000000",
            ),
            "foreign_donor": ColumnMeta(
                description=CAPEX_DICTIONARY["foreign_donor"],
                example="uk",
            ),
            "region": ColumnMeta(
                description=CAPEX_DICTIONARY["region"],
                example="4 demerara/mahaica",
            ),
            "gov_actual_pre_2024": ColumnMeta(
                description=CAPEX_DICTIONARY["gov_actual_pre_2024"],
                unit="GYD",
                example="0",
            ),
            "gov_actual_2024": ColumnMeta(
                description=CAPEX_DICTIONARY["gov_actual_2024"],
                unit="GYD",
                example="0",
            ),
            "gov_actual_2025": ColumnMeta(
                description=CAPEX_DICTIONARY["gov_actual_2025"],
                unit="GYD",
                example="2725000000",
            ),
            "gov_actual_2026": ColumnMeta(
                description=CAPEX_DICTIONARY["gov_actual_2026"],
                unit="GYD",
                example="844163000",
            ),
            "budget_2026": ColumnMeta(
                description=CAPEX_DICTIONARY["budget_2026"],
                unit="GYD",
                example="2844163000",
            ),
        }
    )
}

