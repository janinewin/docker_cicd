import altair as alt
import pandas as pd
import streamlit as st

from app.f1_cache import F1Cache
from app.f1_constants import F1Constants
from app.f1_database import F1Database
from app.f1_queries import F1Queries
from app.f1_transforms import F1Transforms


class F1Dashboard:
    def __init__(self) -> None:
        """Init all the class member needed for the script to render the UI, F1Queries needs its dependencies to be injected"""
        pass  # YOUR CODE HERE

    # TODO Write action
    def layoutSideBar(self):
        """
        Setup UI Side bar with various buttons
        """
        pass  # YOUR CODE HERE

    # TODO Write action
    def clickSideBarButton(self, race_id):
        """
        Action triggered when button click happens, saves race_id into cache and updates is_launched boolean to True
        Parameters
        ----------
        race_id: Int
            id of a given race
        """
        pass  # YOUR CODE HERE

    def layoutHeader(self):
        """
        Setup UI header depending on the launch state of the application, it displays different titles
        """
        pass  # YOUR CODE HERE

    # TODO Write action
    def layoutTopContainer(self):
        """
        Setup top container depending on the launch state of the application. It displays the constructors and drivers standing
        """
        pass  # YOUR CODE HERE

    # TODO Write action
    def layoutMiddleContainer(self):
        """
        Setup middle container depending on the launch state of the application. it displays a few selected metrics showcasing the race
        """
        pass  # YOUR CODE HERE

    def layoutBottomContainer(self):
        """
        Setup bottom container depending on the launch state of the application. It displays a line chart highlighting the evolution of the fastest lap in a race
        """
        # Bottom chart
        fastest_laps = pd.DataFrame()
        pass  # YOUR CODE HERE

        bottom_container = st.container()

        chart = (
            alt.Chart(fastest_laps)
            .mark_line(point=True)
            .encode(
                x=alt.X("lap:Q", axis=alt.Axis(title="Lap number")),
                y=alt.Y("minutesseconds(milliseconds):Q", axis=alt.Axis(title="Time in minutes:s"), scale=alt.Scale(zero=False)),
                #   color=alt.Color("code:N")
            )
            .properties(title="Fastest Lap Evolution")
        )
        bottom_container.altair_chart(chart, use_container_width=True)

    def generateDocString(self, df):
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

    def layoutViews(self):
        """
        Assembles all the views to be presented
        """
        self.layoutSideBar()
        self.layoutHeader()
        self.layoutTopContainer()
        self.layoutMiddleContainer()
        self.layoutBottomContainer()


if __name__ == "__main__":
    dashboard = F1Dashboard()
    dashboard.layoutViews()
