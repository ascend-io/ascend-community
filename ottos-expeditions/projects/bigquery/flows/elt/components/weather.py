import ibis

from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("weather_routes"),
        ref("weather_sensors"),
    ]
)
def weather(
    weather_routes,
    weather_sensors,
    context,
):
    weather = weather_routes.mutate(location=ibis.literal(None, type=str)).union(
        weather_sensors.mutate(
            ascender_id=ibis.literal(None, type=str),
            route_id=ibis.literal(None, type=str),
        )
    )

    return weather
