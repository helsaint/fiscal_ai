from environs import Env
import duckdb
import streamlit as st
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from dataclasses import dataclass
from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field
from pydantic_ai.usage import UsageLimits

# Get environmental variables specifically LLM key
env = Env()
env.read_env()

TOOL_CALL_LIMIT_REACHED = {
    "tool_budget_exhausted": True,
    "message": "Tool call budget exhausted. Finish analysis with existing information."
}

@dataclass
class AnalystDeps:
    conn: duckdb.DuckDBPyConnection
    schema_text: str

    tool_calls: int = 0
    max_tool_call: int = 3

class ColumnSpec(BaseModel):
    name: str = Field(description="Column name exactly as it appears in the table")
    description: str = Field(description="Short human-readable meaning of the column")

class TableSchema(BaseModel):
    table_name: str = Field(description="Name of the table")
    columns: List[ColumnSpec] = Field(description="Columns from this table relevant to the query")
    aggregation_column: str = Field(description="Column from this table to aggregate on")
    aggregation_function: str = Field(description="one of 'sum', 'avg', 'max', 'min', 'count' etc.")

class JoinSchema(BaseModel):
    table_name: str = Field(description="Name of the table")
    column: str = Field(description="Column from this table required for joins")

class FilterSchema(BaseModel):
    table_name: str = Field(description="Name of the table")
    column: str = Field(description="Column on which to apply the filter")
    operator: str = Field(description="Comparison operator to use for the filter ['=', '>', '<', '>=', '<=', '<>']")
    value: Union[str, int, float] = Field(description="Value used for the filter/comparison")

class SchemaPlan(BaseModel):
    relevant_ministry: List[str] = Field(description="The agency or agencies name/s the query is referring to as given in the 'ministry' column of the tables")
    relevant_tables: List[TableSchema] = Field(description="List of table names needed to answer the query.")
    join_logic: Optional[str] = Field(description="Summary of how to join these tables based on the join_hints.")
    joins_column: Optional[List[JoinSchema]] = Field(description="List of table.column required for any joins")
    filter_schema: Optional[List[FilterSchema]] = Field(description="list of filters to apply to each table and the specific columns on which to apply them")
    reasoning: str = Field(description="Short explanation of why these columns were selected.")


class DiscoveryModel:
    def __init__(self, data_dictionary_table="data_dictionary"):
        self.model = self._llm_model_init()
        self.table_name = data_dictionary_table
        self.query_count = 0
        
        # The System Prompt defines the Agent as a Librarian/Router
        self.system_prompt = f"""
        You are a Metadata Librarian. The Metadata is contained in {self.table_name}.
        1 - You only have access to the {self.table_name}
        2 - Do not access any other tables
        3 - you search {self.table_name} and find the names of tables and list of columns that satisfy the user question
        4 - If any tool returns tool_budget_exhausted=True, stop calling tools and produce your best sql query from the evidence already gathered.
        
        Example:
        User: "What is the agriculture opex?"
        Librarian Logic: (Queries dictionary, finds table named 'opex' and the column 'opex_2026')
        Efficiency is priority. Try to find all necessary columns in a SINGLE dictionary search. 
        If you cannot find the columns after two searches, stop and report that the data is missing.

        If you cannot complete the task with data in {self.table_name} just return "Unable to complete".
        Do not try to invent column names and tables that aren't found in {self.table_name}
        """
        
        self.agent = self.__llm_agent_init()
        self.agent.tool(self._query_dictionary)
        self.agent.tool(self._check_tool_budget)
        
        # In a real app, this connection would point to your DuckDB instance
        self.db = duckdb.connect(':memory:') 

    def __llm_agent_init(self):
        # We set result_type to SchemaPlan to enforce the LLM Wiki pattern
        return Agent(
            model=self.model,
            system_prompt=self.system_prompt,
            output_type=SchemaPlan,
        )
    
    def _llm_model_init(self):
        model = OpenAIChatModel(
            'deepseek-chat',
            provider=DeepSeekProvider(api_key=env.str("DEEPSEEK_API_KEY")),
            )
        return model

    async def discover_context(self, question: str) -> SchemaPlan:
        """
        The first pass of the LLM Wiki pattern.
        """
        result = await self.agent.run(question,
                                      model_settings={
                                          "tool_choice": {
                                              "type": "function",
                                              "function": {"name": "_query_database"}
                                              }
                                              },
                                              usage_limits=UsageLimits(request_limit=5))
        return result.output
    
    def test_db(self):
        print("_________________discovery agent v2_____________________________")
        print(self.db.execute("SELECT * FROM DATA_SCHEMA LIMIT 0").fetch_df())

    def _check_tool_budget(self, ctx: RunContext[AnalystDeps]) -> dict[str, Any] | None:
        """ 
        Limit tool calls
        - increments tool_calls counter
        - returns a sentinel payload when max_tool_call limit exceeded
        - does not raise errors
        """
        deps = ctx.deps
        deps.tool_calls += 1
        print("DEPS TOOL CALLS: ", deps.tool_calls)

        if deps.tool_calls > deps.max_tool_call:
            return TOOL_CALL_LIMIT_REACHED
        else:
            return None

    
    async def _query_dictionary(self, ctx: RunContext, keywords: List[str]) -> str:
        """
        Search the data dictionary for relevant tables and columns based on keywords.
        """

        limit = self._check_tool_budget(ctx)
        if limit:
            return limit
        
        # We build a simple search query to prune the 170 columns down
        self.query_count += 1
        search_conditions = " OR ".join([f"description LIKE '%{kw}%' OR columns LIKE '%{kw}%'" for kw in keywords])
        sql = f"SELECT * FROM {self.table_name} WHERE {search_conditions}"
        # Execute against the metadata table
        print("SQL COUNT: ", self.query_count)
        result = self.db.execute(sql).df().to_json()
        if (self.query_count >= 3):
            return "TERMINATE: Limit reached. Use the information already provided to create the SchemaPlan now. Do not call any more tools."
        return result
    
@st.cache_resource
def get_discovery_agent_v2(data_dictionary_table:str):
    return DiscoveryModel(data_dictionary_table)

# Usage in your main app flow:
# 1. discovery_result = await discovery_model.discover_context(user_question)
# 2. Use discovery_result.relevant_columns to filter the dictionary.
# 3. Pass that tiny filtered dictionary to your second 'Execution' agent.