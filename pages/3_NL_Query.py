import streamlit as st
import asyncio

from agents.fiscal_agent_chat_v4 import get_analyst_deps, ChatAgent
#from agents.discovery_agent_v2 import get_discovery_agent_v2, SchemaPlan
from agents.discovery_agent_v3 import get_discovery_agent_v3, SchemaPlan

from app.utils.load_csv import load_csv
from app.utils.data_dictionary import class_to_dict
from app.utils.load_duckdb import get_duckdb
from app.utils.db_connection import QueryDB



from app.utils.sql_creator import sql_creator
import json

from app.utils.temp_example import example_json

def set_column_dict(discovery_agent_dict: dict):
    temp_dict = {}
    for i in discovery_agent_dict['relevant_tables']:
        for j in i['columns']:
            temp_dict[j['name']] = j['description']
    return temp_dict

if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'test_data' not in st.session_state:
    st.session_state.test_data = 0
if 'df_fiscal_smmary' not in st.session_state:
    st.session_state.df_fiscal_summary = None
if 'df_opex' not in st.session_state:
    st.session_state.df_opex = None
if 'df_capex' not in st.session_state:
    st.session_state.df_capex = None
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = None

if st.session_state.df is None:
    df_summary = load_csv("master_ministry_fiscal_intelligence.csv")
    st.session_state.df = df_summary.copy()
    st.session_state.df_fiscal_summary = df_summary.copy()
if st.session_state.df_capex is None:
    df_capex = load_csv("BudgetCapitalExpenditure_vol3_v4.csv")
    st.session_state.df_capex = df_capex.copy()
if st.session_state.df_opex is None:
    df_opex = load_csv("BudgetCurrentExpenditure2026_v3.csv")
    st.session_state.df_opex = df_opex.copy()

discovery_agent = get_discovery_agent_v3(data_dictionary_table="DATA_SCHEMA")
data_schema = class_to_dict()
llm_assistant_4 = ChatAgent()

duckdb_instance = get_duckdb(data_dictionary=data_schema)
duckdb_instance.create_data_schema_db()
#duckdb_instance.test_db()

if "df" in st.session_state and not(st.session_state.data_loaded):

    duckdb_instance.ingest_dataframe(st.session_state.df_fiscal_summary,
                                      "fiscal_summary")
    duckdb_instance.ingest_dataframe(st.session_state.df_capex,
                                      "capex")
    duckdb_instance.ingest_dataframe(st.session_state.df_opex,
                                      "opex")
    st.session_state.db_conn = QueryDB(duckdb_instance)
    
    discovery_agent.db = duckdb_instance
    st.session_state.data_loaded = True

input_message = st.chat_input("Ask a question about the budget")

#discovery_model_v2.test_db()
if input_message:
    discovery_agent.query_count = 0
    with st.chat_message("assistant"):
        discovery_result = asyncio.run(discovery_agent.discover_context(input_message))
        if discovery_result.relevant_tables:
            try:
                sql_query = sql_creator(json.loads(discovery_result.model_dump_json(indent=2)))
                st.write(input_message)
                sql_result = asyncio.run(st.session_state.db_conn.query_db(sql_query))
                temp_dict = set_column_dict(
                    discovery_agent_dict=json.loads(discovery_result.model_dump_json(indent=2)))
                analyst_deps = get_analyst_deps(sql_result, temp_dict)
                final_result = llm_assistant_4.analyze(input_message, analyst_deps=analyst_deps)
                st.write(final_result)
            except:
                st.write("An error occured. Please review your question and try again")
        else:
            st.write(discovery_result.reasoning)



