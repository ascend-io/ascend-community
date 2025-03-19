import snowflake

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(
    inputs=[
        ref("staff"),
        ref("routes"),
        ref("guides"),
        ref("route_closures"),
        ref("telemetry"),
        ref("weather"),
        ref("sales"),
        ref("social_media"),
        ref("feedback"),
    ]
)
def ascenders(
    staff: snowflake.snowpark.Table,
    routes: snowflake.snowpark.Table,
    guides: snowflake.snowpark.Table,
    route_closures: snowflake.snowpark.Table,
    telemetry: snowflake.snowpark.Table,
    weather: snowflake.snowpark.Table,
    sales: snowflake.snowpark.Table,
    social_media: snowflake.snowpark.Table,
    feedback: snowflake.snowpark.Table,
    context: ComponentExecutionContext,
) -> snowflake.snowpark.Table:
    # TODO: more interesting logic here
    return telemetry
