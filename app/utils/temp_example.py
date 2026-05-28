example_json = {
  "relevant_ministry": [
    "ministry of agriculture"
  ],
  "relevant_tables": [
    {
      "table_name": "fiscal_summary",
      "columns": [
        {
          "name": "ministry",
          "description": "The name of the ministry"
        },
        {
          "name": "opex_2026",
          "description": "Budgeted operational expenditure for 2026"
        },
        {
          "name": "capex_2026",
          "description": "Budgeted capital expenditure for 2026"
        },
        {
          "name": "total_spend_2026",
          "description": "Sum of capex_2026 and opex_2026"
        },
        {
          "name": "opex_ratio_budget_2026",
          "description": "Proportion of total 2026 budget allocated to opex"
        },
        {
          "name": "capex_ratio_budget_2026",
          "description": "Proportion of total 2026 budget allocated to capex"
        }
      ],
      "aggregation_column": "ministry",
      "aggregation_function": "none"
    },
    {
      "table_name": "opex",
      "columns": [
        {
          "name": "ministry",
          "description": "The ministry name"
        },
        {
          "name": "account_name",
          "description": "The formal title of the specific expense type"
        },
        {
          "name": "account_description",
          "description": "The formal title of the specific expense type"
        },
        {
          "name": "economic_group",
          "description": "High-level economic classification"
        },
        {
          "name": "economic_subgroup",
          "description": "More granular classification"
        },
        {
          "name": "spending_type",
          "description": "Functional use of the money"
        },
        {
          "name": "cost",
          "description": "Total value for the line item for 2026"
        },
        {
          "name": "budget_2026",
          "description": "Approved funding for 2026 fiscal year"
        },
        {
          "name": "description",
          "description": "Concatenated account code and name"
        }
      ],
      "aggregation_column": "cost",
      "aggregation_function": "sum"
    },
    {
      "table_name": "capex",
      "columns": [
        {
          "name": "ministry",
          "description": "The ministry name"
        },
        {
          "name": "title",
          "description": "Name of the project"
        },
        {
          "name": "description",
          "description": "Short description of project activities"
        },
        {
          "name": "budget_2026",
          "description": "Total budget for 2026 for the project"
        },
        {
          "name": "gov_actual_2026",
          "description": "Government funding budgeted for 2026"
        },
        {
          "name": "foreign_actual_2026",
          "description": "Foreign funding budgeted for 2026"
        }
      ],
      "aggregation_column": "budget_2026",
      "aggregation_function": "sum"
    }
  ],
  "join_logic": "To answer what the Ministry of Agriculture spends most on, we need to look at two angles: (1) For the big picture - use fiscal_summary to see whether the ministry is opex-heavy or capex-heavy (opex_ratio_budget_2026, capex_ratio_budget_2026). (2) For detailed breakdown of operational spending - use the opex table filtered for 'ministry of agriculture' and aggregate by economic_group, spending_type, or account_name to find the largest categories of operational expenditure. (3) For capital spending detail - use capex table filtered by 'ministry of agriculture' and sum budget_2026 by project title to see which projects get the most funding.",
  "joins_column": [
    {
      "table_name": "fiscal_summary",
      "column": "ministry"
    },
    {
      "table_name": "opex",
      "column": "ministry"
    },
    {
      "table_name": "capex",
      "column": "ministry"
    }
  ],
  "filter_schema": [
    {
      "table_name": "opex",
      "column": "ministry",
      "operator": "=",
      "value": "ministry of agriculture"
    },
    {
      "table_name": "capex",
      "column": "ministry",
      "operator": "=",
      "value": "ministry of agriculture"
    }
  ],
  "reasoning": "The question asks what the Ministry of Agriculture spends most of their budget on. This requires: (1) fiscal_summary to understand the high-level split between opex and capex for the ministry (via opex_ratio_budget_2026 and capex_ratio_budget_2026). (2) The opex table to drill down into the detailed operational spending categories by economic_group, spending_type, and account_name/account_description - aggregated by ministry to see which expense categories (e.g., Compensation of Employees, Goods and Services) consume the most funds. (3) The capex table to see which capital projects receive the most funding. The join between fiscal_summary and opex/capex should be on 'ministry' after aggregating opex and capex to ministry level."
}