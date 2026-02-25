import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def load_csv(file_path):
    data_path = Path(__file__).parent.parent.parent / "data" / file_path
    df = pd.read_csv(data_path)
    return df
    
