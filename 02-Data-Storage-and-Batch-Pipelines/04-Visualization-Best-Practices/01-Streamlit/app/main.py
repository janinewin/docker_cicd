import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo = False)

pass  # YOUR CODE HERE
def load_data():
    """
    Loads the data from the csv file.
    Implement the right caching decorator.
    """
    data = pd.read_sql_query("select * from races limit 10", conn)
    return data

def create_main_page():
    pass  # YOUR CODE HERE

def session_state():
    pass  # YOUR CODE HERE

if __name__ == '__main__':
    create_main_page()
    data = load_data()
    st.dataframe(data)
    session_state()
