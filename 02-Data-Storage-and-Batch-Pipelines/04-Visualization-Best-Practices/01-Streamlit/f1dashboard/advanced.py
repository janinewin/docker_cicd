import altair as alt
import pandas as pd
import streamlit as st

from advanced.cache import F1Cache
from advanced.constants import F1Constants
from advanced.database import F1Database
from advanced.queries import F1Queries
from advanced.transforms import F1Transforms


class F1Dashboard:
    def __init__(self) -> None:
        """Init all the class member needed for the script to render the UI, F1Queries needs its dependencies to be injected"""
        self.f1_cache = F1Cache()
        self.f1_transforms = F1Transforms()
        self.f1_database = F1Database()
        self.f1_queries = F1Queries(self.f1_database.db_connection, self.f1_cache)

    def layout_side_bar(self):
        """
        Setup UI Side bar with various buttons
        """
        with st.sidebar:
            st.header("Races")
            for index, race in self.f1_queries.get_races_for_year().iterrows():
                st.button(f'{index+1} - {race["name"]}', on_click=self.click_side_bar_button, args=(race["race_id"],))

    def click_side_bar_button(self, race_id):
        """
        Action triggered when button click happens, saves race_id into cache and updates is_launched boolean to True
        Parameters
        ----------
        race_id: Int
            id of a given race
        """
        self.f1_cache.cache_key_value(F1Constants.IS_LAUNCHED, True)
        self.f1_cache.cache_key_value(F1Constants.SELECTED_RACE, race_id)

    def layout_header(self):
        """
        Setup UI header depending on the launch state of the application, it displays different titles
        """
        if not self.f1_cache.get_value_for_key(F1Constants.IS_LAUNCHED):
            st.title("Welcome to F1's dashboard")
            st.title("2018 championship")
        else:
            header = self.f1_transforms.get_race_name(self.f1_queries.get_races_for_year(), self.f1_cache.get_value_for_key(F1Constants.SELECTED_RACE))
            st.title("2018 championship")
            st.header(header)

    def layout_top_container(self):
        """
        Setup top container depending on the launch state of the application. It displays the constructors and drivers standing
        """
        # Top container
        if not self.f1_cache.get_value_for_key(F1Constants.IS_LAUNCHED):
            constructor_standings = self.f1_queries.get_constructor_standings_for_race(self.f1_queries.get_last_race_id_of_the_year())
            driver_standings = self.f1_queries.getDriverStandingsForRace(self.f1_queries.get_last_race_id_of_the_year())
        else:
            constructor_standings = self.f1_queries.get_constructor_standings_for_race()
            driver_standings = self.f1_queries.getDriverStandingsForRace()

        top_col_left, top_col_right = st.columns(2)
        top_col_left.table(constructor_standings)
        top_col_right.table(driver_standings)

    def layout_middle_container(self):
        """
        Setup middle container depending on the launch state of the application. it displays a few selected metrics showcasing the race
        """
        if not self.f1_cache.get_value_for_key(F1Constants.IS_LAUNCHED):
            return

        fastest_pit_stop = self.f1_queries.get_fastest_pit_stop_for_race()
        fastest_lap = self.f1_queries.get_fastest_lap_time_for_race()
        bottom_col_left, bottom_col_right = st.columns(2)

        bottom_col_left.text("fastest pistop")
        bottom_col_left.text(
            f"""{fastest_pit_stop.iloc[0]['number']} {fastest_pit_stop.iloc[0]['code']} {fastest_pit_stop.iloc[0]['forename']} {fastest_pit_stop.iloc[0]['surname']} {fastest_pit_stop.iloc[0]['duration']}s"""
        )

        bottom_col_right.text("fastest lap")
        bottom_col_right.text(
            f"""{fastest_lap.iloc[0]['number']} {fastest_lap.iloc[0]['code']} {fastest_lap.iloc[0]['forename']} {fastest_lap.iloc[0]['surname']} {fastest_lap.iloc[0]['time']}s"""
        )

    def layout_bottom_container(self):
        """
        Setup bottom container depending on the launch state of the application. It displays a line chart highlighting the evolution of the fastest lap in a race
        """
        # Bottom chart
        fastest_laps = pd.DataFrame()
        if not self.f1_cache.get_value_for_key(F1Constants.IS_LAUNCHED):
            return

        race_laps = self.f1_queries.get_lap_times_for_race()
        fastest_laps = self.f1_transforms.get_best_time_per_lap(race_laps)

        bottom_container = st.container()

        chart = (
            alt.Chart(fastest_laps)
            .mark_line(point=True)
            .encode(
                x=alt.X("lap:Q", axis=alt.Axis(title="Lap number")),
                y=alt.Y("minutesseconds(milliseconds):Q", axis=alt.Axis(title="Time in minutes:s"), scale=alt.Scale(zero=False)),
            )
            .properties(title="Fastest Lap Evolution")
        )
        bottom_container.altair_chart(chart, use_container_width=True)

    def generate_docstring(self, df):
        """
        Generate docstring for a given dataframe

        Parameters
        ----------
        df: pandas.DataFrame
        """

        df = df.copy()
        docstring = "Index:\n"
        docstring = docstring + f"    {df.index}\n"
        docstring = docstring + "Columns:\n"
        for col in df.columns:
            docstring = docstring + f"    Name: {df[col].name}, dtype={df[col].dtype}, nullable: {df[col].hasnans}\n"

        st.write(docstring)
        print(docstring)

    def layout_views(self):
        """
        Assembles all the views to be presented
        """
        self.layout_side_bar()
        self.layout_header()
        self.layout_top_container()
        self.layout_middle_container()
        self.layout_bottom_container()


if __name__ == "__main__":
    dashboard = F1Dashboard()
    dashboard.layout_views()
