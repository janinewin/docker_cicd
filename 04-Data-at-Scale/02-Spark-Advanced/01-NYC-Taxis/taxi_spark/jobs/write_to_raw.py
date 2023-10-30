import argparse
import requests
import shutil
import tempfile

from google.cloud import storage

from taxi_spark.functions.session import get_spark_session
from taxi_spark.functions.schema import enforce_schema


def upload_to_gcs(file_path, bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)


def delete_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def download_and_save_parquet(url: str, bucket: str, date: str) -> None:
    """
    Download a Parquet file from a given URL and save it to Google Cloud Storage.

    :param url: URL to download the Parquet file from.
    :param bucket: Google Cloud Storage bucket to save the downloaded Parquet file.
    :param date: Date for the data, used in naming the saved Parquet file.

    :raises: Exception if any step in the process fails.
    """
    pass  # YOUR CODE HERE


def main() -> None:
    """
    Main function that sets up argument parsing for command-line execution, builds the URL and GCS path,
    and then calls the function to download and save the Parquet file.
    """
    parser = argparse.ArgumentParser(
        description="Download Parquet from a URL and save to GCS."
    )
    parser.add_argument("--date", required=True, help="Date in the format yyyy-MM")
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    args = parser.parse_args()

    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{args.date}.parquet"

    download_and_save_parquet(url, args.bucket, args.date)


if __name__ == "__main__":
    main()
