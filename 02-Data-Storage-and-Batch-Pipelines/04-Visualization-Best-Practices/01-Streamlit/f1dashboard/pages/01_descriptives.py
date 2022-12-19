import pandas as pd
import streamlit as st
from advanced import queries
from advanced.cache import F1Cache
from advanced.database import F1Database
from advanced.queries import F1Queries
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


class DescriptiveStatistics:
    def __init__(self) -> None:
        self.f1_cache = F1Cache()
        self.f1_database = F1Database()
        self.f1_queries = F1Queries(self.f1_database.db_connection, self.f1_cache)

    def select_table(self):
        with st.sidebar:
            st.subheader("Select table to explore")
            self.table_name = st.selectbox(
                "Table name", ["races", "results", "drivers", "constructors"]
            )

    def summary_statistics(self):
        st.title("Descriptive statistics")

        if self.f1_cache.get_value_for_key("results") is self.table_name:
            table_results = self.f1_cache.get_value_for_key("results")
        else:
            table_results = self.f1_queries.retrieve_table(self.table_name)
            self.f1_cache.cache_key_value("results", table_results)

        st.write(table_results.describe())


if __name__ == "__main__":
    data_visualizations = DescriptiveStatistics()
    data_visualizations.select_table()
    data_visualizations.summary_statistics()
