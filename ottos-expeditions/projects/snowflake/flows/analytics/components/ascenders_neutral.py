import snowflake

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("ascenders_analytics")])
def ascenders_neutral(
    ascenders_analytics: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    return ascenders_analytics.sample(0.3)
