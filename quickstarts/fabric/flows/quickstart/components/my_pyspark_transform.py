from pyspark.sql import DataFrame, SparkSession

from ascend.resources import pyspark, ref, test


@pyspark(inputs=[ref("lake_reader")])
def my_pyspark_transform(spark: SparkSession, lake_reader: DataFrame, context) -> DataFrame:
  df = lake_reader.limit(2)
  return df
