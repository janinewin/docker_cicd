import uuid
import pendulum

from airflow.decorators import dag
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator,
)
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)


@dag(
    "spark-pipeline",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["spark"],
)
def spark_pipeline_dag():
    """
    Airflow DAG to execute a Spark pipeline on Google Cloud Dataproc.

    Steps:
    1. `create_dataproc_cluster`: Creates a Dataproc cluster in the specified Google Cloud region.
    2. `copy_wheel_to_gcs`: Copies Python Wheel package to Google Cloud Storage (GCS).
    3. `copy_jobs_to_gcs`: Copies Spark job scripts to GCS.
    4. `write_to_raw`: Executes the Spark job to write raw data to GCS.
    5. `staging_transform`: Executes the Spark job to transform staged data.
    6. `create_processed`: Executes the Spark job to generate processed data.
    7. `delete_dataproc_cluster`: Deletes the Dataproc cluster.

    Parameters:
    - UUID (str): Auto-generated unique identifier for the DAG run.
    - BUCKET_NAME (str): GCS bucket name where data and code are stored.
    - PROJECT (str): Google Cloud Project ID.
    - REGION (str): Dataproc cluster's region.
    - NETWORK (str): VPC network for Dataproc.
    - DATE (str): Data partition identifier (e.g., "2009-01").
    """
    UUID = str(uuid.uuid4())
    BUCKET_NAME = ""
    PROJECT = ""
    REGION = "europe-west1"
    NETWORK = "spark-vpc"
    DATE = "2009-01"
    pass  # YOUR CODE HERE


spark_pipeline_dag()
