import os
import pathlib
import lewagonde

lewagonde.load_dot_env(lewagonde.dot_env_path_sql())
sql_basics_dir = pathlib.Path(os.path.dirname(__file__)).parent

# For execution in ipython
# hardcoded_file = "/Users/nicolasbancel/git/lewagon/data-engineering-solutions/02-Data-Storage-and-Batch-Pipelines/02-SQL/02-SQL-Basics/tests/test_exercice_4_1_1.py"
# sql_basics_dir = pathlib.Path(os.path.dirname(hardcoded_file)).parent

exercice_4_2 = os.path.join(sql_basics_dir, "exercice-4-2.sql")

with open(exercice_4_2, "r") as f:
    df_4_2 = lewagonde.read_sql_query(
        f.read(),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        user="lewagon",
        host="localhost",
        dbname="db",
    )


def test_referential_integrity():
    columns_set = set(df_4_2.columns)
    assert columns_set == set(["movie_id_ratings_table"]), "Column name of the output is incorrect"

    problematic_record_example_1 = df_4_2[df_4_2["movie_id_ratings_table"] == 1014]
    assert len(problematic_record_example_1) == 1, "movie_id = 1014 is a problematic record - it should appear in your result, only 1 time"

    problematic_record_example_2 = df_4_2[df_4_2["movie_id_ratings_table"] == 112064]
    assert len(problematic_record_example_2) == 1, "movie_id = 112064 is a problematic record - it should appear in your result, only 1 time"

    assert len(df_4_2) == 37550, "There should be a total of 37550 records that are failing (37550 movie_ids in ratings that don't exist in movies_metadata"
