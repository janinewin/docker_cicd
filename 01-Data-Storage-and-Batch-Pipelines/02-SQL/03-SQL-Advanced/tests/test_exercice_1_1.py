import os
import pathlib
import lewagonde

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/01-Data-Storage-and-Batch-Pipelines/02-SQL/03-SQL-Advanced/tests/test_exercice_1_1.py"
# sql_advanced_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercice_1_1 = os.path.join(sql_advanced_dir, "exercice-1-1.sql")

with open(exercice_1_1, "r") as f:
    df_1_1 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )


def test_correct_columns():
    assert set(["id", "profit_absolute", "profit_percentage"]) <= set(df_1_1.columns), "Some key columns are missing, or are mispelled"


def test_correct_filters():
    assert len(df_1_1) == 5381, "Your filtering is incorrect - the output should display 5381 records"
