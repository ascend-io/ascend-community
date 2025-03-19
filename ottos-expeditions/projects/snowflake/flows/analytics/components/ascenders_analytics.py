import snowflake

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("alias_ascenders")])
def ascenders_analytics(
    alias_ascenders: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    ascenders_analytics = alias_ascenders
    return ascenders_analytics
