from google.cloud import storage
from datetime import datetime
import os


def check_bucket_exists(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket.exists()


def check_blob_exists(bucket_name, blob_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    return blob.exists()


def test_bucket_exists():
    bucket_name = os.environ.get("LAKE_BUCKET")
    assert bucket_name, "LAKE_BUCKET environment variable not set!"
    assert check_bucket_exists(bucket_name), f"Bucket {bucket_name} does not exist!"


def test_blob_exists():
    bucket_name = os.environ.get("LAKE_BUCKET")
    assert bucket_name, "LAKE_BUCKET environment variable not set!"
    date_str = datetime.now().strftime("%Y/%m/%d")
    blob_path = f"raw/hackernews/stories/{date_str}/stories.csv"
    assert check_blob_exists(
        bucket_name, blob_path
    ), f"Blob {blob_path} does not exist in bucket {bucket_name}!"
