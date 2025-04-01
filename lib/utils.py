import os
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, DataFrame

def get_spark_app_config() -> SparkConf:
    """
    Returns a SparkConf object with any custom Spark settings you need.
    You can customize these configurations based on your environment.
    """
    conf = SparkConf()
    # Basic example settings (customize as needed)
    conf.set("spark.app.name", "HelloSparkApp")
    # conf.set("spark.executor.memory", "2g")
    # conf.set("spark.executor.cores", "2")
    # Add or modify additional Spark configs as required
    return conf

def load_zip_df(spark: SparkSession, csv_path: str) -> DataFrame:
    """
    Loads a CSV file into a Spark DataFrame, using `spark.read`.
    Adjust options (inferSchema, header) as needed.
    """
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(csv_path)
    return df
