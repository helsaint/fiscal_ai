"""
from engine.fiscal_tools import FiscalTools

tools = FiscalTools()

print(tools.national_spending_summary())
print(tools.top_spending_ministries(5))
print(tools.low_outcome_ministries())
print(tools.foreign_dependent_ministries())
"""

"""
from agents.fiscal_agent import FiscalAgent

temp = FiscalAgent()
"""
from engine.loader import FiscalDataLoader
from engine.fiscal_core.unified_truth_engine import UnifiedTruthEngine
from agents.fiscal_analyst_agent import FiscalAnalystAgent
from agents.cabinet_briefing_agent import CabinetBriefingAgent
from agents.expenditure_review_agent import ExpenditureReviewAgent
from environs import Env

env = Env()
env.read_env()

datasets = FiscalDataLoader().load_ministry_summary()

review_agent = ExpenditureReviewAgent(
    datasets.ministry_summary, 
    env.str("CHATGPT_API_KEY")
    )

print(review_agent.start_review("ministry of health"))

print(review_agent.ask("What are the main efficiency concerns?"))
print(review_agent.ask("Drill into capex execution risk."))
print(review_agent.ask("Is this a candidate for budget reduction?"))
