import datetime
from typing import List, Tuple
import pandas as pd


def str2timestamp(str_datetime, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """Converts a datetime string into a unix timestamp(number of seconds 1/1/1970 00:00:00)"""
    dt = datetime.datetime.strptime(str_datetime, fmt)
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def strtime_window_rounded(str_datetime, window=15, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """
    Converts a datetime to rounded datetime with a frequency window in sec
    """
    timestamp = str2timestamp(str_datetime, fmt)
    timestamp_rounded = (timestamp // window + 1) * window
    datetime_rounded = datetime.datetime.utcfromtimestamp(timestamp_rounded)
    return datetime_rounded.strftime(fmt)


def aggregate_sensors(timestamp: str, sensor_values: List[List[Tuple]]):
    pass  # YOUR CODE HERE
