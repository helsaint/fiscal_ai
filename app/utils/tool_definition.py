{
  "name": "get_fiscal_data",
  "description": "Queries the fiscal database for specific ministries or agency types. Use this to retrieve budget, performance, and risk metrics.",
  "parameters": {
    "type": "object",
    "properties": {
      "target_type": {
        "type": "string",
        "enum": ["single_ministry", "agency_type_group", "global_outliers"],
        "description": "Whether to fetch data for one ministry, a whole sector (e.g., Military), or the top/bottom performers."
      },
      "identifier": {
        "type": "string",
        "description": "The name of the ministry or the agency_type. Leave blank for 'global_outliers'."
      },
      "columns": {
        "type": "array",
        "items": { "type": "string" },
        "description": "List of specific columns needed. Examples: 'opex_2026', 'fiscal_risk_score', 'budget_pressure_flag'."
      },
      "sort_by": {
        "type": "string",
        "description": "Column to sort by if requesting outliers or groups."
      }
    },
    "required": ["target_type", "columns"]
  }
}