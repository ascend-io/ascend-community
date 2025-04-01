import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("weather_routes"),
        ref("weather_sensors"),
    ]
)
def weather(
    weather_routes: ibis.Table,
    weather_sensors: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    weather = weather_routes.mutate(location=ibis.literal(None, type=str)).union(
        weather_sensors.mutate(
            ascender_id=ibis.literal(None, type=str),
            route_id=ibis.literal(None, type=str),
        )
    )

    return weather
