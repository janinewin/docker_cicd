import os
import pathlib

import lewagonde

# import read_sql_query, load_dot_env, constants

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
df_columns = lewagonde.read_sql_query(
    "SELECT * \
    FROM INFORMATION_SCHEMA.COLUMNS \
    WHERE table_name IN ('movies_metadata', 'ratings') \
    ",
    password=os.environ.get("POSTGRES_PASSWORD", ""),
    user="lewagon",
    host="localhost",
    dbname="db",
)

adult_column = df_columns[(df_columns["table_name"] == "movies_metadata") & (df_columns["column_name"] == "adult")]
video_column = df_columns[(df_columns["table_name"] == "movies_metadata") & (df_columns["column_name"] == "video")]
timestamp_column = df_columns[(df_columns["table_name"] == "ratings") & (df_columns["column_name"] == "timestamp")]
blablabla_column = df_columns[(df_columns["table_name"] == "ratings") & (df_columns["column_name"] == "blablabla")]
created_at_utc_column = df_columns[(df_columns["table_name"] == "ratings") & (df_columns["column_name"] == "created_at_utc")]


def test_correct_column_names():
    assert len(adult_column) == 1, "adult column in movies_metadata table not loaded - or incorrectly spelled"
    assert len(video_column) == 1, "video column in movies_metadata table not loaded - or incorrectly spelled"
    assert len(timestamp_column) == 1, "timestamp column in ratings table not loaded - or incorrectly spelled"


def test_correct_column_types():
    assert len(adult_column[adult_column["data_type"] == "boolean"]) == 1, "adult column in movies_metadata table has not been converted to correct data type"
    assert len(video_column[video_column["data_type"] == "boolean"]) == 1, "video column in movies_metadata table has not been converted to correct data type"
    assert len(created_at_utc_column) == 1, "created_at_utc column in ratings table not created - or incorrectly spelled"
    # Conversion can also be, if no timezone : timestamp without time zone
    assert (
        len(created_at_utc_column[created_at_utc_column["data_type"].str.contains("timestamp")]) == 1,
        "created_at_utc in ratings table has not been converted to correct data type",
    )
