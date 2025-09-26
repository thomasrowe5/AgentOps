import streamlit as st
import pandas as pd
from pathlib import Path

st.title("AgentOps Dashboard")

p = Path("data/metrics.csv")
if p.exists():
    df = pd.read_csv(p)
    st.write("Latest metrics:")
    st.dataframe(df.tail(20))
    st.line_chart(df["total_time"])
else:
    st.info("No metrics yet. Run the workflow baseline first.")
