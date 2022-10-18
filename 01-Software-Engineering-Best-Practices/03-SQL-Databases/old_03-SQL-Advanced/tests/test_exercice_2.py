import os
import pathlib
import lewagonde

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-Storage-and-Batch-Pipelines/02-SQL/03-SQL-Advanced/tests/test_exercice_2.py"
# sql_advanced_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercice_2 = os.path.join(sql_advanced_dir, "exercice-2.sql")

with open(exercice_2, "r") as f:
    df_2 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )


def test_correct_columns_and_size():
    expected_columns = set(["release_year", "avg_revenue", "avg_profit_absolute", "avg_profit_perc"])
    assert expected_columns == set(df_2.columns), "Some key columns are missing, or are mispelled"

    dataset_size = len(df_2)
    assert dataset_size == 98, "The output should surface values for 98 years - spanning over 1916 until 2017"


def test_correct_metric_calculation():
    avg_revenue_2015 = df_2[df_2["release_year"] == 2015].reset_index()["avg_revenue"][0]
    assert avg_revenue_2015 == 138426029, "Average revenue in 2015 is wrong - should be 138426029"

    avg_profit_absolute_2015 = df_2[df_2["release_year"] == 2015].reset_index()["avg_profit_absolute"][0]
    assert avg_profit_absolute_2015 == 100001337, "Average absolute profit in 2015 is wrong - should be 100001337"

    avg_profit_perc_2015 = df_2[df_2["release_year"] == 2015].reset_index()["avg_profit_perc"][0]
    assert avg_profit_perc_2015 == 2.89, "Average profit perc in 2015 is wrong - should be 2.89"
