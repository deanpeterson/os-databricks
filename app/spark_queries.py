from pyspark.sql import SparkSession, DataFrame
from lib.utils import get_spark_app_config, load_zip_df
import os

def create_spark_session(app_name="HelloSpark") -> SparkSession:
    conf = get_spark_app_config()
    spark = SparkSession.builder \
        .master("local[*]") \
        .config(conf=conf) \
        .appName(app_name) \
        .getOrCreate()
    return spark

def filter_zipcodes(csv_path: str, zipcode: int):
    spark = create_spark_session()
    zip_df = load_zip_df(spark, csv_path)
    filtered_zips = zip_df.where(f"Zipcode = {zipcode}")
    result = filtered_zips.collect()
    spark.stop()
    return [row.asDict() for row in result]
