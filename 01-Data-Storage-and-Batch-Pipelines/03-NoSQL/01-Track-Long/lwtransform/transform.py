import argparse
import ast
import os
import pathlib
from typing import Dict, List, Tuple

import pandas as pd

MOVIES_METADATA_NORMALIZED_COLUMNS = [
    "adult",
    "budget",
    "homepage",
    "id",
    "imdb_id",
    "original_language",
    "original_title",
    "overview",
    "popularity",
    "poster_path",
    "release_date",
    "revenue",
    "runtime",
    "status",
    "tagline",
    "title",
    "video",
    "vote_average",
    "vote_count",
]

TAGS_COLUMNS = ["name", "value"]

TAGS_MAP_COLUMNS = ["movie_id", "tag_name", "tag_value"]

# Helper functions
##################

def int_or_zero(v):
    """
    Cast a value to `int` or 0
    """
    return int(v) if not pd.isna(v) and (isinstance(v, float) or isinstance(v, int)) else 0


def float_or_zero(v):
    """
    Cast a value to `float` or 0.0
    """
    return float(v) if not pd.isna(v) and (isinstance(v, float) or isinstance(v, int)) else 0.0


def bool_or_false(v):
    """
    Cast a value to `bool` or False
    """
    return v if isinstance(v, bool) else False


# Data loader
#############

def load_and_clean_movies(movies_metadata_csv_fp: str) -> pd.DataFrame:
    """
    Loads and cleans the `movies_metadata` CSV given its filepath `movies_metadata_csv_fp`.
    """
    movies_df = pd.read_csv(movies_metadata_csv_fp)

    # Keep only integer `id` rows
    movie_id_int = movies_df["id"].str.isnumeric()

    # Cast vote_count as integer
    movies_df["vote_count"] = movies_df["vote_count"].apply(int_or_zero)

    # Cast adult as boolean
    movies_df["adult"] = movies_df["adult"].apply(bool_or_false)

    # Cast budget as float
    movies_df["budget"] = movies_df["budget"].apply(float_or_zero)

    return movies_df.loc[movie_id_int, :].reset_index()


def parse_list_column(l_col_value: str):
    """
    In the `movies_metadata` CSV, lists are stored as Python lists, with single quotes instead of double quotes.
    This makes them non-JSON compatible.
    We use the Python AST to parse the strings to Python lists.
    """
    if pd.isna(l_col_value):
        return []
    literal = ast.literal_eval(l_col_value)
    if not isinstance(literal, list):
        return []
    return literal


def extract_tags(id_column: pd.Series, links_column: pd.Series, identifier_key: str, value_key: str):
    """
    The list columns are always a list of Python `dict` with two keys, an ID ("id" or "iso_...") which we call `identifier_key,
    and a name which we call `value_key`.

    Args:
      - `id_columns`: the column with the movie ID, as a `pandas.Series`
      - `links_column`: the column with the Python lists, which we call "links"
      - `identifier_key`: like "id"
      - `value_key`: like "name"

    Returns:
      A tuple made of the list of unique tags, and a DataFrame with the `movie_id` and associated `tag_value`.
      Note the `movie_id` will appear as many tiimes as its number of associated tags.
    """
    keyed_options = {}
    movie_to_links = []
    for movie_id, links in zip(id_column, links_column):
        for value in links:
            keyed_options[value[identifier_key]] = value[value_key]
            movie_to_links.append((movie_id, value[value_key]))
    return list(keyed_options.values()), pd.DataFrame(movie_to_links, columns=["movie_id", "tag_value"])


def extract_lists(movies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Turns the 'string list' columns into actual Python lists.
    """
    genres_list = movies_df["genres"].apply(parse_list_column)
    production_companies_list = movies_df["production_companies"].apply(parse_list_column)
    production_countries_list = movies_df["production_countries"].apply(parse_list_column)
    spoken_languages_list = movies_df["spoken_languages"].apply(parse_list_column)
    return genres_list, production_companies_list, production_countries_list, spoken_languages_list 


def make_tags_df(tag_name_and_values: Dict[str, List[str]]):
    """
    Args:
      - `tag_name_and_values`: dictionary where
        - the key is the name of the tag, like "production_country"
        - the value is the list of unique tags like ["United States", "Zambia"]

    Returns:
      - a `pandas.DataFrame` with columns `["name", "value"]`
    """
    rows = []
    for tag_name, values in tag_name_and_values.items():
        for value in values:
            rows.append((tag_name, value))
    return pd.DataFrame(rows, columns=["name", "value"])


def make_tags_map_df(tag_name_and_values: Dict[str, pd.DataFrame]):
    """
    Args:
      - `tag_name_and_values`: dictionary where:
        - the key is the name of the tag, like "production_country"
        - the value is a DataFrame with columns "movie_id" and "tag_value"

    Returns:
      - a `pandas.DataFrame` with columns `["movie_id", "tag_value", "tag_name"]`
    """
    final_df = pd.DataFrame([], columns=["movie_id", "tag_value", "tag_name"])
    for tag_name, df in tag_name_and_values.items():
        df["tag_name"] = tag_name
        final_df = pd.concat([final_df, df], copy=False)
    return final_df


def make_new_tables(original_movies_df: pd.DataFrame, genres_list, production_companies_list, production_countries_list, spoken_languages_list) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Given the cleaned `movies_df`, concatenates the new flat `tags` and `tags_map` DataFrame

    Returns:
      - Tuple `(tags_df, tags_map_df)`
    """
    movies_df = original_movies_df.copy()
    movies_df["genres_list"] = genres_list
    movies_df["production_companies_list"] = production_companies_list
    movies_df["production_countries_list"] = production_countries_list
    movies_df["spoken_languages_list"] = spoken_languages_list

    mapping = [
        {"col": "genres_list", "key": "id", "val": "name", "name": "genre"},
        {"col": "production_companies_list", "key": "id", "val": "name", "name": "production_company"},
        {"col": "production_countries_list", "key": "iso_3166_1", "val": "name", "name": "production_country"},
        {"col": "spoken_languages_list", "key": "iso_639_1", "val": "name", "name": "spoken_language"},
    ]

    options = {}
    dfs = {}
    for item in mapping:
        all_options, df = extract_tags(movies_df["id"], movies_df[item["col"]], item["key"], item["val"])
        options[item["name"]] = all_options
        dfs[item["name"]] = df

    tags_df = make_tags_df(options)
    tags_map_df = make_tags_map_df(dfs)

    return tags_df, tags_map_df


def save_new_tables_to_csvs(output_dir: str, tags_df: pd.DataFrame, tags_map_df: pd.DataFrame, original_movies_df: pd.DataFrame):
    """
    Store the newly created tables to the right place
    """
    tags_df.to_csv(os.path.join(output_dir, "tags.csv"), index=False, columns=TAGS_COLUMNS)
    tags_map_df.to_csv(os.path.join(output_dir, "tags_map.csv"), index=False, columns=TAGS_MAP_COLUMNS)
    original_movies_df.to_csv(os.path.join(output_dir, "movies_metadata_normalized.csv"), index=False, columns=MOVIES_METADATA_NORMALIZED_COLUMNS)


def movies_to_new_tables(raw_movies_metadata_csv_fp: str, output_dir: str):
    """
    Takes the raw movies metadata CSV, cleans it, breaks it down into
    """
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    original_movies_df = load_and_clean_movies(raw_movies_metadata_csv_fp)
    genres_list, production_companies_list, production_countries_list, spoken_languages_list = extract_lists(original_movies_df)
    tags_df, tags_map_df = make_new_tables(original_movies_df, genres_list, production_companies_list, production_countries_list, spoken_languages_list)

    # Store the `movies_metadata_normalized.csv`, `tags.csv` and `tags_map.csv` files in the `output_dir` by adding code below 
    pass  # YOUR CODE HERE


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--movies", required=True, help="Raw movies CSV filepath")
    parser.add_argument("--out", required=True, help="Output directory")
    return parser.parse_args()


if __name__ == "__main__":
    _args = parse_args()
    movies_to_new_tables(raw_movies_metadata_csv_fp=_args.movies, output_dir=_args.out)
