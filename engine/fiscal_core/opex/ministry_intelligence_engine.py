import pandas as pd

# df is dataset from the BudgetCurrentExpenditure2026_v3.csv
# ministry is the ministry of interest from the drop down in 4_Ministry_Opex_Review.py
# Uses the data to create a profile for the ministry

def build_ministry_profile(df: pd.DataFrame, ministry: str) -> dict:
    rows = df[df["ministry"] == ministry]

    if rows.empty:
        raise ValueError(f"Ministry '{ministry}' not found.")
    
    profile = {
        "ministry": ministry,

        # Structural Spend
        "budgeted_spend_year_0": rows["budget_2026"].sum(),
        "actual_spend_year_1": rows["revised_2025"].sum(),
        "actual_spend_year_2": rows["actual_2024"].sum(),

        # High Level Fiscal Indicators
        "budget_credibility_ratio": (rows["revised_2025"].sum()/rows["budget_2025"].sum())*100,

        # Budget growth rate
        "budget_growth_yoy": [100*(rows["revised_2025"].sum()/rows["actual_2024"].sum() - 1), 
                              100*(rows["budget_2026"].sum()/rows["revised_2025"].sum() - 1)],
        
        "cagr": ((rows["budget_2026"].sum()/rows["actual_2024"].sum())**(0.5)-1)*100,

        # Rigidity distribution
        "rigidity_distribution": rows.groupby('rigidity')[
            'budget_2026'
            ].sum().to_dict(),

        # Spending by type
        "spending_type": rows.groupby('spending_type')[
            'budget_2026'
        ].sum().to_dict(),

        # Personnel and Operations cost
        "personnel_cost": rows[
            rows['spending_type'] == 'Personnel'
            ][
                ['actual_2024', 'revised_2025', 'budget_2026']
                ].sum().to_dict(),

        "operations_cost": rows[
            rows['spending_type'] == 'Operations'
            ][
                ['actual_2024', 'revised_2025', 'budget_2026']
                ].sum().to_dict(),

        "economic_group_costs": rows.groupby('economic_group')[
            'budget_2026'
        ].sum().to_dict(),
    }
    print(rows.columns)
    print("--------------------")
    #print(profile)
    #print(rows['spending_type'].unique())
    #print(rows['economic_subgroup'].unique())
    #print(rows['account_name'].unique())

    return profile