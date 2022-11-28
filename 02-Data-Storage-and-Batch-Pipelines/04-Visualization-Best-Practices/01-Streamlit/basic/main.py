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
    Returns:
        pd.DataFrame: The race dataset
    """
    data = pd.read_sql_query("select * from races limit 10", conn)
    return data

def create_main_page():
    """
    Creates the following Streamlit headers:
    - A title
    - A subheader
    - A title in the sidebar
    - A markdown section in the sidebar
    """
    st.title("Formula 1 Dashboard")
    pass  # YOUR CODE HERE

def session_state(data):
    """
    Initialize the session state
    using data as the key and value as the
    initialization value.

    Put data in the session state after having
    initialized it.

    Args:
        data (pd.DataFrame): The formula 1 dataset
    """

    # Initialization of session state
    pass  # YOUR CODE HERE

    # Update the session state using the dataframe
    pass  # YOUR CODE HERE

if __name__ == '__main__':
    create_main_page()
    data = load_data()
    st.dataframe(data)
    session_state(data)
