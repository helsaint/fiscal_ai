import streamlit as st

st.set_page_config(
    page_title="Fiscal Intelligence System",
    layout="wide"
)

st.title("Fiscal Intelligence System")

st.markdown("""
Internal Treasury Analytical Platform

Use the sidebar to navigate between system modules.
""")

with st.sidebar:
    st.page_link("home.py", label="Home", icon="🏠")
    st.page_link("pages/1_Fiscal_Dashboard.py", label="Fiscal Dashboard", icon="📊")
    st.page_link("pages/2_Ministry_Review.py", label="Ministry Review", icon="📑")
    st.page_link("pages/3_NL_Query.py", label="Natural Language Querying", icon="📑")
    st.page_link("pages/4_Ministry_Opex_Review.py", label="Ministry OPEX Review", icon="📊")
