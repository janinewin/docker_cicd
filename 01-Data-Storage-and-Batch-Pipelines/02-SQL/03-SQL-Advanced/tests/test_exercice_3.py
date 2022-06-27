import os
import pathlib
import lewagonde

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/01-Data-Storage-and-Batch-Pipelines/02-SQL/03-SQL-Advanced/tests/test_exercice_3.py"
# sql_advanced_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercice_3 = os.path.join(sql_advanced_dir, "exercice-3.sql")

with open(exercice_3, "r") as f:
    df_3 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )


def test_correct_columns_and_size():
    expected_columns = set(["release_year", "avg_profit_perc", "avg_profit_perc_growth_yoy", "avg_profit_absolute", "avg_profit_absolute_growth_yoy"])
    assert expected_columns == set(df_3.columns), "Some key columns are missing, or are mispelled"