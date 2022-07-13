import json
import pathlib
import os

import pandas as pd
from pandas.api import types as ptypes

import lewagonde

from lwdb import db


def prep_db():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")
    lewagonde.load_dot_env(dot_env_fp)


def test_datafile():
    """
    Tests that the raw datafile is present
    """
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    data_fp = os.path.join(parent_dir, "data", "ikea-raw.json")
    assert os.path.isfile(data_fp), "File data/ikea-raw.json not found"


def test_csv_raw():
    """
    Test that the generated CSV is present
    """
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    pq_fp = os.path.join(parent_dir, "data", "ikea-raw.parquet")
    df = pd.read_parquet(pq_fp)
    columns = set([
        "product_title", "product_url", "sku", "mpn", "currency", "product_price",
        "product_condition", "availability", "seller", "seller_url", "brand", "raw_product_details",
        "breadcrumbs", "country", "language", "average_rating", "reviews_count",
    ])
    assert set(df.columns) == columns, f"Wrong columns in the CSV, expected {columns}"


def test_csv_cleaned():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    csv_fp = os.path.join(parent_dir, "data", "ikea-cols.csv")
    assert os.path.isfile(csv_fp), f"File {csv_fp} not present, fill in `cast_columns` then call `save_df_to_csv`"
    df = pd.read_parquet(csv_fp)
    assert ptypes.is_numeric_dtype(df.product_price) and ptypes.is_numeric_dtype(df.average_rating) and ptypes.is_int64_dtype(df.reviews_count), "product_price, average_rating must have numeric types and reviews_count be integer"


def test_table_creation():
    prep_db()
    df = lewagonde.read_sql_query("SELECT * FROM ikea_products LIMIT 1;", password=os.environ["POSTGRES_PASSWORD"], user="lewagon", host="0.0.0.0", dbname="db")
    columns = set([
        "product_title", "product_url", "sku", "mpn", "currency", "product_price",
        "product_condition", "availability", "seller", "seller_url", "brand", "raw_product_details",
        "breadcrumbs", "country", "language", "average_rating", "reviews_count",
    ])
    assert columns <= set(df.columns), f"Wrong columns in the table, expected {columns}"


def test_data_loaded():
    """
    Test that the CSV was loaded in the DB with the right schema
    """
    df = lewagonde.read_sql_query("SELECT COUNT(*) AS count FROM ikea_products;", password=os.environ["POSTGRES_PASSWORD"], user="lewagon", host="0.0.0.0", dbname="db")
    assert df["count"].iloc[0] > 10000, "Data doesn't seem to be loaded"


def test_q1_v1():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    sql_file_path = os.path.join(parent_dir, "sql", "q1-v1-select-sku.sql")
    _, results = db.query_perf(sql_file_path=sql_file_path)
    assert results.shape[0] == 1, "q1-v1 query seems wrong, we should find one result"
    assert results.iloc[0]["sku"] == "605.106.40", "q1-v1 query seems wrong, we should find one result with SKU '605.106.40'"


def test_q2_v1():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    sql_file_path = os.path.join(parent_dir, "sql", "q2-v1-search-chair.sql")
    _, results = db.query_perf(sql_file_path=sql_file_path)
    assert results.iloc[0, 0] > 25, "q2-v1 query seems wrong, we should find more than 25 results"


def test_btree_index():
    """
    Test that a BTree index on the SKU was added
    """
    _, results = db.query_perf(sql_query="select count(*) as count from pg_indexes where indexname = 'index_sku';")
    assert results.iloc[0]["count"] == 1, "BTree index not added, make sure to name it 'index_sku'"


def text_fulltext():
    """
    Test that a full text search index on the raw_product_details was added
    """
    _, results = db.query_perf(sql_query="select count(*) as count from pg_indexes where indexname = 'index_raw_product_details_text';")
    assert results.iloc[0]["count"] == 1, "Full text index not found, name it 'index_raw_product_details_text'"


def test_q2_v2():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    sql_file_path = os.path.join(parent_dir, "sql", "q2-v2-search-chair.sql")
    _, results = db.query_perf(sql_file_path=sql_file_path)
    assert results.iloc[0, 0] > 25, "q2-v2 query seems wrong, finding less than 25 values, expected more"


def test_perf():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    perf_file_path = os.path.join(parent_dir, "perf.json")
    with open(perf_file_path) as f:
        perf = json.load(f)["timings_milliseconds"]
    assert perf["q1-select-sku"]["v1"] != 0 and perf["q1-select-sku"]["with_index"] != 0 and perf["q2-search-chair"]["v1"] != 0 and perf["q2-search-chair"]["v2"] != 0, "Perf.json isn't fully filled out"
    assert perf["q1-select-sku"]["v1"] > perf["q1-select-sku"]["with_index"], "q1-select-sku v1 should perform worse than with_index, did you fill perf.json"
    assert perf["q2-search-chair"]["v1"] > perf["q2-search-chair"]["v2"], "q2-search-chair v1 should perform worse than v2, did you fill perf.json"
