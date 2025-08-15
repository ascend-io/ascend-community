import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(
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
    staff: ibis.Table,
    routes: ibis.Table,
    guides: ibis.Table,
    route_closures: ibis.Table,
    telemetry: ibis.Table,
    weather: ibis.Table,
    sales: ibis.Table,
    social_media: ibis.Table,
    feedback: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    # TODO: more interesting logic here
    return telemetry
