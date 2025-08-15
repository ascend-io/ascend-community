from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import pyspark, ref
from pyspark.sql import DataFrame, SparkSession


@pyspark(
    inputs=[
        ref("ascenders", flow="transform"),
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
