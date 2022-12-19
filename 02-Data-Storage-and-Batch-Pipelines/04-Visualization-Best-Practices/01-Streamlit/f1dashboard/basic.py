import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo=False)

pass  # YOUR CODE HERE
def load_data():
    """
    Loads the races data from the F1 database.
    Implement the right caching decorator.
    Returns:
        pd.DataFrame: The race dataset
    """
    data = pd.read_sql_query("select * from races", conn)
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


def summary_statistics(data):
    """
    Creates a subheader and writes the summary statistics for the data
    """
    st.subheader("Summary statistics")
    pass  # YOUR CODE HERE


@st.experimental_memo
def top_drivers():
    """
    Get the top 5 drivers with the most points.
    You can get the name from the drivers table and
    combine it with the points from the driver_standings table.
    Returns:
        pd.DataFrame: The top 5 drivers with the columns:
                      - driver_name
                      - total_points
    """
    top_drivers = "Write a query to get the top 5 drivers and visualize the results."
    pass  # YOUR CODE HERE
    return lewis_points


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


if __name__ == "__main__":
    create_main_page()

    data = load_data()
    st.dataframe(data)

    summary_statistics(data)
    session_state(data)

    st.subheader("session state data")
    st.write(st.session_state["data"])

    st.subheader("Top 5 Drivers")
    top_driver_data = top_drivers()
    st.write(top_driver_data)

    # create a bar chart with the top drivers, you can use the Altair library
    pass  # YOUR CODE HERE

    st.subheader("Lewis Hamilton over the years")
    lewis_years = lewis_over_the_years()
    st.write(lewis_years)

    # create a line chart with lewis_years, use the Altair library
    pass  # YOUR CODE HERE
