import streamlit as st
from pathlib import Path

def local_css(file_name):
    data_path = Path(__file__).parent.parent.parent / "app" / "static" / file_name
    with open(data_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)