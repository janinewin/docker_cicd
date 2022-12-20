import pandas as pd
import streamlit as st

from app.f1_cache import F1Cache
from app.f1_constants import F1Constants

__all__ = ["F1Queries"]


class F1Queries:
    def __init__(self, databaseConnection, f1Cache: F1Cache) -> None:
        self.conn = databaseConnection
        self.f1_cache = f1Cache

    # # Perform query.
    # # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)
    def _run_query(_self, query):
        """
        Base utility method queries a database using pandas and returning a dataframe

        Parameters
        ----------
        query: Str
            SQL query as a f-string

        Returns
        -------
        races: pandas.DataFrame
            Dataframe containing the result of the query

        """

        return pd.read_sql_query(query, _self.conn)

    def getRacesForYear(self, year=2018):
        """
        Queries DB for the last race id for a given year.

        Parameters
        ----------
        year: Int
            year to query the db for
            if not provided default to 2018

        Returns
        -------
        races: pandas.DataFrame
            Dataframe containing all the races for a given year

            Index:
                RangeIndex
            Columns:
                Name: race_id, dtype=int64, nullable: False
                Name: year, dtype=int64, nullable: False
                Name: round, dtype=int64, nullable: False
                Name: circuit_id, dtype=int64, nullable: False
                Name: name, dtype=object, nullable: False
                Name: date, dtype=object, nullable: False
                Name: time, dtype=object, nullable: False
                Name: url, dtype=object, nullable: False

        """

        races = self._run_query(
            f"""
        SELECT
        *
        FROM races
        WHERE year={year}
        ORDER BY round ASC
        """
        )

        return races

    def getLastRaceIdOfTheYear(self, year=2018):
        """
        Queries DB for the last race id for a given year.

        Parameters
        ----------
        year: Int
            year to query the db for
            if not provided default to 2018

        Returns
        -------
        race_id: Int
            Last id of a race in a given year
        """

        race_id = self._run_query(
            f"""
        SELECT
        race_id
        FROM races
        WHERE year={year}
        ORDER BY round DESC
        LIMIT 1
        """
        ).iloc[0]["race_id"]

        return race_id

    def getConstructorStandingsForRace(self, race_id=None):
        """
        Queries DB for the constructor standings for a given race.

        Parameters
        ----------
        raced_id: Int
            id of a given race
            if `None` it will use the cache to get the actual value

        Returns
        -------
        constructor_standings_df: pandas.DataFrame
            Dataframe containing the constructor standings for a given race

            Index:
                RangeIndex
            Columns:
                Name: name, dtype=object, nullable: False
                Name: points, dtype=float64, nullable: False
                Name: wins, dtype=int64, nullable: False

        """
        if not race_id:
            race_id = self.f1_cache.getValueForKey(F1Constants.SELECTED_RACE)

        constructor_standings_df = self._run_query(
            f"""SELECT
            position
            , points
            , wins
            , name
            , nationality
            FROM constructor_standings
            JOIN constructors
            ON constructor_standings.constructor_id = constructors.constructor_id
            WHERE race_id={race_id}
            ORDER BY points DESC
            """
        )[["name", "points", "wins"]]

        return constructor_standings_df

    def getDriverStandingsForRace(self, race_id=None):
        """
        Queries DB for the driver standings for a given race,

        Parameters
        ----------
        raced_id: Int
            id of a given race
            if `None` it will use the cache to get the actual value

        Returns
        -------
        driver_standings_df: pandas.DataFrame
            Dataframe containing the driver standings for a given race

            Index:
                RangeIndex: Int64
            Columns:
                Name: code, dtype=object, nullable: False
                Name: forename, dtype=object, nullable: False
                Name: surname, dtype=object, nullable: False
                Name: points, dtype=float64, nullable: False
                Name: wins, dtype=int64, nullable: False

        """
        if not race_id:
            race_id = self.f1_cache.getValueForKey(F1Constants.SELECTED_RACE)

        driver_standings_df = self._run_query(
            f"""SELECT
            position
            , points
            , wins
            , number
            , code
            , forename
            , surname
            , nationality
            FROM driver_standings
            JOIN drivers
            ON driver_standings.driver_id = drivers.driver_id
            WHERE race_id={race_id}
            ORDER BY points DESC
            """
        )[["code", "forename", "surname", "points", "wins"]]

        return driver_standings_df

    def getFastestPitStopForRace(self):
        """
        Queries DB for all the lap times for a given race

        Returns
        -------
        fastest_pistop_df: pandas.DataFrame
            Dataframe containing the fastest pit stop for a given race

            Index:
                RangeIndex(start=0, stop=1, step=1)
            Columns:
                Name: lap, dtype=int64, nullable: False
                Name: duration, dtype=object, nullable: False
                Name: number, dtype=int64, nullable: False
                Name: code, dtype=object, nullable: False
                Name: forename, dtype=object, nullable: False
                Name: surname, dtype=object, nullable: False

        """

        race_id = self.f1_cache.getValueForKey(F1Constants.SELECTED_RACE)
        fastest_pistops = self._run_query(
            f"""
            SELECT
            lap
            , duration
            , number
            , code
            , forename
            , surname
            FROM pit_stops
            INNER JOIN drivers
            ON pit_stops.driver_id = drivers.driver_id
            INNER JOIN races
            ON pit_stops.race_id = races.race_id
            WHERE races.race_id = {race_id}
            ORDER BY milliseconds ASC
            LIMIT 1
            """
        )

        return fastest_pistops

    def getFastestLapTimeForRace(self):
        """
        Queries DB for the fastest lap time for a given race

        Returns
        -------
        fastest_lap_df: pandas.DataFrame
            Dataframe containing the fastest lap for a given race

            Index:
                RangeIndex([...])
            Columns:
                Name: time, dtype=object, nullable: False
                Name: milliseconds, dtype=int64, nullable: False
                Name: number, dtype=int64, nullable: False
                Name: code, dtype=object, nullable: False
                Name: forename, dtype=object, nullable: False
                Name: surname, dtype=object, nullable: False
                Name: race_id, dtype=int64, nullable: False

        """

        race_id = self.f1_cache.getValueForKey(F1Constants.SELECTED_RACE)
        fastest_lap_df = self._run_query(
            f"""
            SELECT
            lap_times.time
            , milliseconds
            , number
            , code
            , forename
            , surname
            , lap_times.race_id
            FROM lap_times
            INNER JOIN drivers
            ON lap_times.driver_id = drivers.driver_id
            INNER JOIN races
            ON lap_times.race_id = races.race_id
            WHERE races.race_id = {race_id}
            ORDER BY milliseconds ASC
            LIMIT 1
            """
        )

        return fastest_lap_df

    def getLapTimesForRace(self):
        """
        Queries DB for all the lap times for a given race

        Returns
        -------
        laps_df: pandas.DataFrame
            Dataframe containing the laps of all drivers for a given race

            Index:
                RangeIndex([...])
            Columns:
                Name: lap, dtype=int64, nullable: False
                Name: code, dtype=object, nullable: False
                Name: milliseconds, dtype=int64, nullable: False
                Name: time, dtype=object, nullable: False
                Name: number, dtype=int64, nullable: False
                Name: forename, dtype=object, nullable: False
                Name: surname, dtype=object, nullable: False

        """
        race_id = self.f1_cache.getValueForKey(F1Constants.SELECTED_RACE)
        laps_df = self._run_query(
            f"""
            SELECT
            lap
            , position
            , lap_times.time
            , milliseconds
            , number
            , code
            , forename
            , surname
            FROM lap_times
            JOIN drivers
            ON lap_times.driver_id = drivers.driver_id
            WHERE race_id={race_id}
            """
        )[["lap", "code", "milliseconds", "time", "number", "forename", "surname"]]

        return laps_df


if __name__ == "__main__":
    queries = F1Queries()
