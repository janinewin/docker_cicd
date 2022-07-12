import pathlib
import os

import pandas as pd
from pandas.api import types as ptypes


def test_datafile():
    """
    Tests that the raw datafile is present
    """
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    data_fp = os.path.join(parent_dir, "data", "ikea-raw.json")
    assert os.path.isfile(data_fp)


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
    pq_fp = os.path.join(parent_dir, "data", "ikea-cols.parquet")
    assert os.path.isfile(pq_fp), f"File {pq_fp} not present, fill in `cast_columns` then call `save_df_to_csv`"
    df = pd.read_parquet(pq_fp)
    assert ptypes.is_numeric_dtype(df.product_price) and ptypes.is_numeric_dtype(df.average_rating) and ptypes.is_int64_dtype(df.reviews_count), "product_price, average_rating must have numeric types and reviews_count be integer"


def test_table_creation():
    import lewagonde
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")
    lewagonde.load_dot_env(dot_env_fp)
    df = lewagonde.read_sql_query("SELECT * FROM ikea_products LIMIT 1;", password=os.environ["POSTGRES_PASSWORD"], user="lewagon", host="0.0.0.0", dbname="db")
    columns = set([
        "product_title", "product_url", "sku", "mpn", "currency", "product_price",
        "product_condition", "availability", "seller", "seller_url", "brand", "raw_product_details",
        "breadcrumbs", "country", "language", "average_rating", "reviews_count",
    ])
    assert set(df.columns) == columns, f"Wrong columns in the table, expected {columns}"


def test_data_loaded():
    """
    Test that the CSV was loaded in the DB with the right schema
    """
    import lewagonde
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    dot_env_fp = os.path.join(parent_dir, ".env")
    lewagonde.load_dot_env(dot_env_fp)
    df = lewagonde.read_sql_query("SELECT COUNT(*) AS count FROM ikea_products;", password=os.environ["POSTGRES_PASSWORD"], user="lewagon", host="0.0.0.0", dbname="db")
    assert df["count"].iloc[0] > 10000


def test_btree_index():
    """
    Test that a BTree index on the SKU was added
    """
    pass


def text_fulltext():
    """
    Test that a full text search index on the raw_product_details was added
    """
    pass


def test_schema_rewrite():
    """
    Test that a materialized view was created
    """
    pass
