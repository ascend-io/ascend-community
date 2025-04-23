from pyspark.sql import DataFrame, SparkSession

from ascend.resources import ref, pyspark
from ascend.common.events import log
from ascend.application.context import ComponentExecutionContext


@pyspark(
    inputs=[
        ref("ascenders", flow="transform-databricks"),
    ]
)
def ascenders_pyspark(
    spark: SparkSession,
    ascenders: DataFrame,
    context: ComponentExecutionContext,
) -> DataFrame:
    df = ascenders
    log(f"Rows: {df.count()}")
    return df
