import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("./data/wikipedia_data.csv")
    df["summary"] = df["summary"].apply(lambda x: x.replace("\n","\n\n"))
    return df