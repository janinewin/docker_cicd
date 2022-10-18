import os
import pathlib
import lewagonde

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
sql_advanced_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-Storage-and-Batch-Pipelines/02-SQL/03-SQL-Advanced/tests/test_exercice_1_1.py"
# sql_advanced_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercice_1_2 = os.path.join(sql_advanced_dir, "exercice-1-2.sql")

with open(exercice_1_2, "r") as f:
    df_1_2 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )


def test_correct_filters():
    assert len(df_1_2) == 5121, "Your filtering is incorrect - the output should display 5121 records"


def test_correct_metric_calculation():
    bambi_profit_absolute = df_1_2[df_1_2["id"] == 3170].reset_index()["profit_absolute"][0]
    assert bambi_profit_absolute == 266589150.0, "Profit absolute calculation incorrect"

    bambi_profit_percentage = df_1_2[df_1_2["id"] == 3170].reset_index()["profit_percentage"][0]
    assert bambi_profit_percentage == 310.71, "Profit percentage calculation incorrect - did you round up to 2 decimals ?"
