import altair as alt
import streamlit as st
from advanced.cache import F1Cache


class DataVisualizations:
    def __init__(self) -> None:
        self.f1_cache = F1Cache()

    def top_drivers(self):
        st.subheader("Top 5 Drivers")

        top_drivers_data = self.f1_cache.get_data("top_drivers")

        bar_chart = alt.Chart(top_drivers_data).mark_bar().encode(y="total_points", x="driver_name")

        st.altair_chart(bar_chart, use_container_width=True)

    def lewis_hamilton_over_the_years(self):
        st.subheader("Lewis Hamilton over the years")

        lewis_years = self.f1_cache.get_data("lewis_over_the_years")

        # create a line chart with lewis_years, use the Altair library
        line_chart = alt.Chart(lewis_years).mark_line().encode(y="total_points", x="year")

        st.altair_chart(line_chart, use_container_width=True)


if __name__ == "__main__":
    st.title("Data visualizations")
    data_visualizations = DataVisualizations()
    data_visualizations.top_drivers()
    data_visualizations.lewis_hamilton_over_the_years()
