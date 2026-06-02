from environs import Env
from dataclasses import dataclass
from typing import Dict, List, Any
import pandas as pd
import streamlit as st
from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai import Agent, RunContext

env = Env()
env.read_env()

TOOL_CALL_LIMIT_REACHED = {
    "tool_budget_exhausted": True,
    "message": "Tool call budget exhausted. Finish analysis with existing information."
}

@dataclass
class AnalystDeps:
    df: pd.DataFrame
    column_metadata: Dict[str, str]

    tool_calls: int = 0
    max_tool_call: int = 5
    max_rows: int = 20

class ChatAgent:
    def __init__(self):
        self.model = self._llm_model_init()
        self.agent = self._llm_agent_init()

        self.agent.tool(self._get_column_metadata)
        self.agent.tool(self._get_descriptive_stats)
        self.agent.tool(self._get_ordered_data)
        self.agent.tool(self._get_pivot_table)

    def analyze(self, prompt: str, analyst_deps: AnalystDeps):
        result = self.agent.run_sync(prompt, deps=analyst_deps)
        return result.output
        

    def _llm_model_init(self):
        model = OpenAIChatModel(
            'deepseek-chat',
            provider=DeepSeekProvider(api_key=env.str("DEEPSEEK_API_KEY")),
            )
        return model
    
    def _llm_agent_init(self):
        agent = Agent(
            model=self.model,
            deps_type=AnalystDeps,
            system_prompt= (
            "You are a government budget data analyst.\n"
            "Use the tools to inspect the dataset.\n"
            "If any tool returns tool_budget_exhausted=True, stop calling tools "
            "and produce your best final analysis from the evidence already gathered."
            ),
            )

        #agent.system_prompt(self._get_dynamic_metadata)
        return agent
    
    def _get_descriptive_stats(self, ctx: RunContext[AnalystDeps]) -> Dict[str, Any]:
        """ Returns descriptive statistics for object and numeric columns"""
        limit = self._check_tool_budget(ctx)
        if limit:
            return limit
        
        df = ctx.deps.df[:ctx.deps.max_rows]
        num_stats = df.describe().to_dict()
        obj_stats = df.describe(include='object').to_dict()
        return {"numeric columns": num_stats, "categorical and string data": obj_stats}

    def _get_column_metadata(self, ctx: RunContext[AnalystDeps]) -> Dict[str, str]:
        """ Return column names and their descriptions."""
        limit = self._check_tool_budget(ctx)
        if limit:
            return limit
        
        return ctx.deps.column_metadata
    
    def _get_pivot_table(self, ctx:RunContext[AnalystDeps], index_list: List[str],
                         aggregation_columns: List[str]):
        """ 
        Return a dataframe as a dictionary pivoted on index_list column and 
        aggregated on aggregation_columns. The aggregation will be summation
        """
        limit = self._check_tool_budget(ctx)
        if limit:
            return limit
        
        df = ctx.deps.df
        df_pivot = pd.pivot_table(df, index=index_list, values=aggregation_columns,
                                  aggfunc='sum')
        df_pivot = df_pivot.sort_values(by=aggregation_columns, ascending=False)
        return df_pivot[:ctx.deps.max_rows].to_dict()
    
    def _get_ordered_data(self, ctx: RunContext[AnalystDeps], columns: List[str]) -> dict:
        """ Return dataframe as a dictionary ordered by the columns."""
        limit = self._check_tool_budget(ctx)
        if limit:
            return limit
        
        df = ctx.deps.df.sort_values(by=columns, ascending=False)
        df = df[:ctx.deps.max_rows]
        
        return df.to_dict()
    
    def _check_tool_budget(self, ctx: RunContext[AnalystDeps]) -> dict[str, Any] | None:
        """ 
        Limit tool calls
        - increments tool_calls counter
        - returns a sentinel payload when max_tool_call limit exceeded
        - does not raise errors
        """
        deps = ctx.deps
        deps.tool_calls += 1

        if deps.tool_calls > deps.max_tool_call:
            return TOOL_CALL_LIMIT_REACHED
        else:
            return None
    
def get_analyst_deps(df:pd.DataFrame, column_meta: dict):
    return AnalystDeps(df, column_meta)