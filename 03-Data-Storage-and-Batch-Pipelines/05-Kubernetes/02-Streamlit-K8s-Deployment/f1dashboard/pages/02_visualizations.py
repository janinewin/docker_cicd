import altair as alt
import streamlit as st
from advanced.cache import F1Cache
import pandas as pd

class DataVisualizations:
    def __init__(self) -> None:
        self.f1_cache = F1Cache()

    def top_drivers(self):
        """Create a bar chart with the top 5 drivers
        """

        st.subheader("Top 5 Drivers")

        top_driver_data = self.f1_cache.get_data("top_drivers")

        pass  # YOUR CODE HERE

    def lewis_hamilton_over_the_years(self):
        """Create a line chart with the points of Lewis Hamilton over the years
        """
        st.subheader("Lewis Hamilton over the years")

        lewis_years = self.f1_cache.get_data("lewis_over_the_years")

        lewis_years['year'] = pd.to_datetime(lewis_years['year'],format='%Y')

        # create a line chart with lewis_years, use the Altair library
        pass  # YOUR CODE HERE


if __name__ == "__main__":
    st.title("Data visualizations")
    data_visualizations = DataVisualizations()
    data_visualizations.top_drivers()
    data_visualizations.lewis_hamilton_over_the_years()
