from pyspark.sql import DataFrame, functions as F


def add_time_bins(df: DataFrame) -> DataFrame:
    """
    Add a 'time_bin' column to DataFrame based on the hour of 'trip_pickup_datetime'.

    morning = 5-11
    afternoon = 12-17
    evening = 18-22
    night = 23-4

    Parameters:
    - df (DataFrame): Input DataFrame with a 'trip_pickup_datetime' column.

    Returns:
    - DataFrame: DataFrame with an additional 'time_bin' column.
    """
    pass  # YOUR CODE HERE


def add_pickup_date(df: DataFrame) -> DataFrame:
    """
    Add a 'pickup_date' column to DataFrame by extracting the date from 'trip_pickup_datetime'.

    Parameters:
    - df (DataFrame): Input DataFrame with a 'trip_pickup_datetime' column.

    Returns:
    - DataFrame: DataFrame with an additional 'pickup_date' column.
    """
    pass  # YOUR CODE HERE


def drop_coordinates(df: DataFrame) -> DataFrame:
    """
    Drop coordinate columns from DataFrame.

    Parameters:
    - df (DataFrame): Input DataFrame with 'start_lon', 'start_lat', 'end_lon', 'end_lat' columns.

    Returns:
    - DataFrame: DataFrame without the coordinate columns.
    """
    pass  # YOUR CODE HERE


def aggregate_metrics(df: DataFrame) -> DataFrame:
    """
    Aggregate metrics like average fare, total passengers, etc., by 'pickup_date' and 'time_bin'.

    Parameters:
    - df (DataFrame): Input DataFrame with 'pickup_date', 'time_bin', 'fare_amt', 'passenger_count', and 'haversine_distance'.

    Returns:
    - DataFrame: DataFrame with aggregated metrics: 'avg_fare', 'total_passengers', 'total_trips' and 'avg_distance'.
    """
    pass  # YOUR CODE HERE


def sort_by_date_and_time(df: DataFrame) -> DataFrame:
    """
    Sort DataFrame by 'pickup_date' and 'time_bin'.

    Parameters:
    - df (DataFrame): Input DataFrame with 'pickup_date' and 'time_bin' columns.

    Returns:
    - DataFrame: DataFrame sorted by 'pickup_date' and 'time_bin' in ascending order.
    """
    pass  # YOUR CODE HERE
