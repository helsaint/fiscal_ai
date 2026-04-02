import streamlit as st
import asyncio
from agents.fiscal_agent_chat_v2 import get_llm_instance
from app.utils.load_csv import load_csv
from app.utils.system_prompt import system_prompt

if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'test_data' not in st.session_state:
    st.session_state.test_data = 0

df_summary = load_csv("master_ministry_fiscal_intelligence.csv")
st.session_state.df = df_summary.copy()

llm_assistant = get_llm_instance(system_prompt=system_prompt)

if "df" in st.session_state and not(st.session_state.data_loaded):
    llm_assistant.ingest_dataframe(st.session_state.df)
    st.session_state.data_loaded = True

input_message = st.chat_input("Ask a question about the data")

if input_message:
    with st.chat_message("assistant"):
        # Since 'ask' is async, we use asyncio to run it
        llm_assistant.test_db()
        st.session_state.test_data += 1
        print(st.session_state.test_data)
        response = asyncio.run(llm_assistant.ask(input_message))
        st.write(response)