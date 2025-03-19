import snowflake

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(
    inputs=[
        ref("ascenders"),
        ref("routes"),
        ref("telemetry"),
    ]
)
def goats(
    ascenders: snowflake.snowpark.Table,
    routes: snowflake.snowpark.Table,
    telemetry: snowflake.snowpark.Table,
    context: ComponentExecutionContext,
) -> snowflake.snowpark.Table:
    return ascenders.sample(0.01)
