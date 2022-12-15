import streamlit as st
import pandas as pd
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import altair as alt

from basic import load_data, top_drivers, lewis_over_the_years

conn_string = URL.create(**st.secrets["postgres"])
conn = create_engine(conn_string, echo = False)

data = load_data()

st.title("Data visualizations")
st.subheader("Top 5 Drivers")

top_driver_data = top_drivers()

# create a bar chart with the top drivers, you can use the Altair library
bar_chart = alt.Chart(top_driver_data).mark_bar().encode(
    y='total_points',
    x='driver_name')

st.altair_chart(bar_chart, use_container_width=True)

st.subheader("Lewis Hamilton over the years")
lewis_years = lewis_over_the_years()

# create a line chart with lewis_years, use the Altair library
# $CHALLENGIFY_BEGIN
line_chart = alt.Chart(lewis_years).mark_line().encode(
    y='total_points',
    x='year')

st.altair_chart(line_chart, use_container_width=True)
