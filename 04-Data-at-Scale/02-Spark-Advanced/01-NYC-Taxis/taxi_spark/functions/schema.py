from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType


def enforce_schema(df):
    """
    Enforces a specific schema on a given DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame to enforce the schema on.

    Returns:
    - DataFrame: The original DataFrame if the schema matches.

    Raises:
    - AssertionError: If the DataFrame schema does not match the expected schema.
    """
    pass  # YOUR CODE HERE
    return df
