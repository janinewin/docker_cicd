import os
import pathlib
import lewagonde

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
sql_basics_dir = pathlib.Path(os.path.dirname(__file__)).parent
# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-Storage-and-Batch-Pipelines/02-SQL/02-SQL-Basics/tests/test_exercice_4_1_1.py"
# sql_basics_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent
exercice_4_1_1 = os.path.join(sql_basics_dir, "exercice-4-1-1.sql")

with open(exercice_4_1_1, "r") as f:
    df_4_1_1 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )


def test_duplicate_movies_metadata():
    columns_set = set(df_4_1_1.columns)
    assert columns_set == set(["id", "num_records"]), "Column names of the output are incorrect"

    duplicate_example = df_4_1_1[df_4_1_1["id"] == 25541]
    assert len(duplicate_example) == 1, "Your output should include id = 25541, which is duplicated in the table"

    assert len(df_4_1_1) == 29, "There should be 29 duplicated IDs in the movies_metadata table"
