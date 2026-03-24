import streamlit as st
import pandas as pd
from pathlib import Path
import hashlib

@st.cache_data
def load_csv(file_path):
    data_path = Path(__file__).parent.parent.parent / "data" / file_path
    df = pd.read_csv(data_path)
    return df

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    data_path = Path(__file__).parent.parent.parent / "data" / file_path
    with open(data_path, "rb") as f:
        # Read in chunks to handle large datasets without RAM spikes
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
