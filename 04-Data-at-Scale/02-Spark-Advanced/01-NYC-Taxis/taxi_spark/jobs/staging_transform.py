import argparse


from taxi_spark.functions.session import get_spark_session
from taxi_spark.functions.calculations import (
    calculate_trip_duration,
    calculate_haversine_distance,
)
from taxi_spark.functions.cleaning import (
    remove_duplicates,
    handle_nulls,
    type_casting,
    normalize_strings,
    format_dates,
    filter_coordinates,
    rename_columns,
)


def staging_pipeline(raw_uri: str, staging_uri: str) -> None:
    """
    Processes a raw Parquet dataset and writes the cleaned data to a staging URI.

    :param raw_uri: URI of the raw Parquet dataset.
    :param staging_uri: URI where the processed Parquet dataset will be saved.

    Steps:
    - Reads Parquet data from `raw_uri`.
    - Removes duplicates.
    - Handles null values.
    - Performs type casting.
    - Normalizes strings.
    - Formats dates.
    - Filters coordinates.
    - Calculates trip duration.
    - Calculates haversine distance.
    - Renames columns.
    - Writes processed data to `staging_uri`.
    """
    pass  # YOUR CODE HERE


def main() -> None:
    """
    Main function that sets up argument parsing for command-line execution, builds the URL and GCS path,
    and then calls the function to download and save the Parquet file.
    """
    parser = argparse.ArgumentParser(
        description="Preprocess the raw data and save it to the staging area in GCS"
    )
    parser.add_argument("--date", required=True, help="Date in the format yyyy-MM")
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    args = parser.parse_args()

    raw_uri = f"gs://{args.bucket}/raw/taxi_data/yellow_tripdata_{args.date}.parquet"
    staging_uri = f"gs://{args.bucket}/staging/taxi_data/yellow_tripdata_{args.date}"

    staging_pipeline(raw_uri, staging_uri)


if __name__ == "__main__":
    main()
