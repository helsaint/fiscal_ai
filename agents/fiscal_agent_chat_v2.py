from environs import Env
import duckdb
import re
import streamlit as st
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from dataclasses import dataclass

# Get environmental variables specifically LLM key
env = Env()
env.read_env()

class ChatModel:
    def __init__(self, system_prompt):
        self.model = self._llm_model_init()
        self.duck_db_conn = duckdb.connect(':memory:')
        self.system_prompt = system_prompt
        self.agent = self.__llm_agent_init()

        self.agent.tool(self.query_database)

    async def ask(self, question:str):
        result = await self.agent.run(question,
                                      model_settings={
                                          "tool_choice": {
                                              "type":"function",
                                              "function": {"name" : "query_database"}
                                          }
                                      })
        return result.output
    
    async def query_database(self, ctx: RunContext, sql: str) -> str:
        return self._execute_sql(sql)

    def __llm_agent_init(self):
        agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt,
        )
        return agent

    def _llm_model_init(self):
        model = OpenAIChatModel(
            'deepseek-chat',
            provider=DeepSeekProvider(api_key=env.str("DEEPSEEK_API_KEY")),
            )
        return model
    
    def ingest_dataframe(self, df):
        table_name = "master_ministry_fiscal_intelligence"
        #self.duck_db_conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
        self.duck_db_conn.register(table_name, df)

    def test_db(self):
        print(self.duck_db_conn.execute("SELECT * FROM master_ministry_fiscal_intelligence LIMIT 3").fetchdf())

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
def get_llm_instance(system_prompt:str):
    return ChatModel(system_prompt=system_prompt)



