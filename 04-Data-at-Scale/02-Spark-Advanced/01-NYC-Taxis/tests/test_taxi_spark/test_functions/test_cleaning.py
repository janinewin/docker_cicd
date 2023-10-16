from taxi_spark.functions.cleaning import (
    remove_duplicates,
    handle_nulls,
    type_casting,
    normalize_strings,
    format_dates,
    filter_coordinates,
    rename_columns,
)
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    FloatType,
    TimestampType,
)


def test_remove_duplicates(spark):
    pass  # YOUR CODE HERE


def test_handle_nulls(spark):
    pass  # YOUR CODE HERE


def test_type_casting(spark):
    pass  # YOUR CODE HERE


def test_normalize_strings(spark):
    pass  # YOUR CODE HERE


def test_format_dates(spark):
    pass  # YOUR CODE HERE


def test_filter_coordinates(spark):
    pass  # YOUR CODE HERE


def test_rename_columns(spark):
    # $CHALLENGIFY_BEGIN
    df = spark.createDataFrame([(1,)], ["a b"])
    df = rename_columns(df)
    assert "a_b" in df.columns
    # $CHALLENGIFY_BEGIN
