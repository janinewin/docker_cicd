from pyspark.sql import SparkSession
import os


def get_spark_session():
    spark_builder = SparkSession.builder.appName("Taxifare PySpark App")

    if os.environ.get("LOCAL"):
        spark_builder = (
            spark_builder.config(
                "spark.hadoop.fs.gs.impl",
                "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
            )
            .config("spark.hadoop.fs.gs.project.id", os.environ["PROJECT_ID"])
            .config(
                "spark.hadoop.google.cloud.auth.service.account.json.keyfile",
                "/home/oliver.giles/.config/gcloud/application_default_credentials.json",
            )
            .config(
                "spark.jars",
                "/home/oliver.giles/spark/jars/gcs-connector-hadoop3-latest.jar",
            )
        )

    return spark_builder.getOrCreate()
