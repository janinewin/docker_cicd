import streamlit as st
import pandas as pd
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine


from basic import load_data, summary_statistics

conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo = False)

data = load_data()

pass  # YOUR CODE HERE
