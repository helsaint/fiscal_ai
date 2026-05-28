from environs import Env
import duckdb
import re
import streamlit as st
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from dataclasses import dataclass
import pandas as pd
from typing import Dict

# Get environmental variables specifically LLM key
env = Env()
env.read_env()

from dataclasses import dataclass

@dataclass
class AnalystDeps:
    df: pd.DataFrame
    column_metadat: Dict[str, str]

class ChatModel:
    def __init__(self, system_prompt):
        self.model = self._llm_model_init()
        self.duck_db_conn = duckdb.connect(':memory:')
        self.system_prompt = system_prompt
        self.agent = self.__llm_agent_init()
        self.query_count = 0

        self.agent.tool(self._query_database)

    async def ask(self, question:str):
        print("SYSTEM_PROMPT: ", self.agent.system_prompt)
        result = await self.agent.run(question,
                                      model_settings={
                                          "tool_choice": {
                                              "type":"function",
                                              "function": {"name" : "_query_database"}
                                          }
                                      },
                                      #usage_limits=UsageLimits(request_limit=10)
                                      )
        return result.output
        
    
    async def _query_database(self, ctx: RunContext, sql: str) -> str:
        self.query_count += 1
        print("Second Stage query count: ", self.query_count)
        print("SQL: ", sql)
        '''
        if (self.query_count >= 3):
            return "TERMINATE: Limit reached. Use the information already provided to answer the user question"
        '''
        return self._execute_sql(sql)

    def __llm_agent_init(self):
        agent = Agent(
            model=self.model,
            deps_type=str,
        )
        return agent
    
    
    def set_system_prompt(self, system_prompt: str):
        #self.agent.system_prompt = system_prompt
        self.agent.instructions = system_prompt

    def _llm_model_init(self):
        model = OpenAIChatModel(
            'deepseek-chat',
            provider=DeepSeekProvider(api_key=env.str("DEEPSEEK_API_KEY")),
            )
        return model

    def test_db(self):
        #print(self.duck_db_conn.execute("SELECT * FROM master_ministry_fiscal_intelligence LIMIT 3").fetchdf())
        print("___________________________Fiscal Agent Chat_________________________________________")
        print(self.duck_db_conn.execute("SELECT table_name, description FROM DATA_SCHEMA").fetch_df())

    def _execute_sql(self, query:str) -> str:
        pattern = re.compile(r"^\s*select\b", re.IGNORECASE)
        if not pattern.match(query):
            return "Security Violation: Non-SELECT query detected."
        
        try:
            result = self.duck_db_conn.execute(query).fetchdf()
            if result.empty:
                return "No results."
            return result.to_string(index=False)
        except Exception as e:
            return f"Error: {str(e)}"
        return ""
    
@st.cache_resource
def get_llm_instance_v3(system_prompt:str):
    return ChatModel(system_prompt=system_prompt)