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
    Airflow DAG for executing a Spark pipeline on Google Cloud Dataproc.

    Steps:
    1. Copies Python Wheel package to GCS: `copy_wheel_to_gcs`
    2. Copies job scripts to GCS: `copy_jobs_to_gcs`
    3. Executes write to raw data job: `write_to_raw_batch`
    4. Transforms staging data: `staging_transform_batch`
    5. Creates processed data: `create_processed_batch`

    Parameters:
    - UUID: Unique identifier for the DAG run.
    - BUCKET_NAME: Google Cloud Storage bucket name.
    - PROJECT: Google Cloud Project ID.
    - REGION: Google Cloud Region for Dataproc.
    - NETWORK: VPC network for Dataproc.
    - DATE: Data partition identifier.

    """
    pass  # YOUR CODE HERE


spark_pipeline_dag()
