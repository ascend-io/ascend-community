import snowflake.snowpark as sp
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, snowpark, test


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
    ],
    tests=[
        test("count_greater_than_or_equal", count=0, severity="error"),
    ],
)
def ascenders(
    staff: sp.Table,
    routes: sp.Table,
    guides: sp.Table,
    route_closures: sp.Table,
    telemetry: sp.Table,
    weather: sp.Table,
    sales: sp.Table,
    social_media: sp.Table,
    feedback: sp.Table,
    context: ComponentExecutionContext,
) -> sp.Table:
    # TODO: more interesting logic here
    return telemetry
