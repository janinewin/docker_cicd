import streamlit as st
from advanced.cache import F1Cache
from advanced.constants import F1Constants
from advanced.database import F1Database
from advanced.queries import F1Queries


class DescriptiveStatistics:
    def __init__(self) -> None:
        """Initialize the class"""
        self.f1_cache = F1Cache()
        self.f1_database = F1Database()
        self.f1_queries = F1Queries()

    def select_table(self):
        """Select the table to explore"""
        with st.sidebar:
            st.subheader("Select table to explore")
            self.selected_table = "races"
            pass  # YOUR CODE HERE

    def summary_statistics(self):
        """Use the describe method to get the summary statistics"""
        st.title("Descriptive statistics")

        if self.selected_table in st.session_state:
            st.info(f"Retrieve the {self.selected_table} table from cache")
            table_results = self.f1_cache.get_data_from_cache(self.selected_table)
        else:
            st.info(f"Retrieve the {self.selected_table} table from the database")
            table_results = self.f1_queries.retrieve_table(self.selected_table)
            self.f1_cache.store_in_cache(self.selected_table, table_results)

        # describe the table_results data
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    data_visualizations = DescriptiveStatistics()
    data_visualizations.select_table()
    data_visualizations.summary_statistics()
