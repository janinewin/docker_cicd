import altair as alt
import pandas as pd
import streamlit as st
from advanced import queries
from advanced.cache import F1Cache
from advanced.database import F1Database
from advanced.queries import F1Queries
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


class DataVisualizations:
    def __init__(self) -> None:
        self.f1_cache = F1Cache()
        self.f1_database = F1Database()
        self.f1_queries = F1Queries(self.f1_database.db_connection, self.f1_cache)
        st.title("Data visualizations")

    def top_drivers(self):
        st.subheader("Top 5 Drivers")

        if self.f1_cache.get_value_for_key("top_5_drivers") is not None:
            top_drivers_data = self.f1_cache.get_value_for_key("top_5_drivers")
        else:
            top_drivers_data = self.f1_queries.top_drivers()
            self.f1_cache.cache_key_value("top_5_drivers", top_drivers_data)

        # create a bar chart with the top drivers, you can use the Altair library
        bar_chart = (
            alt.Chart(top_drivers_data)
            .mark_bar()
            .encode(y="total_points", x="driver_name")
        )

        st.altair_chart(bar_chart, use_container_width=True)

    def lewis_hamilton_over_the_years(self):
        st.subheader("Lewis Hamilton over the years")

        if self.f1_cache.get_value_for_key("lewis_years") is not None:
            lewis_years = self.f1_cache.get_value_for_key("lewis_years")
            st.write("Retrieved the data from cache")
        else:
            lewis_years = self.f1_queries.lewis_over_the_years()
            self.f1_cache.cache_key_value("lewis_years", lewis_years)

        # create a line chart with lewis_years, use the Altair library
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    data_visualizations = DataVisualizations()
    data_visualizations.top_drivers()
    data_visualizations.lewis_hamilton_over_the_years()
