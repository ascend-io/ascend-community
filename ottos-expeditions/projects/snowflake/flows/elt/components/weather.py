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
    weather = weather_routes.mutate(LOCATION=ibis.literal(None, type=str)).union(
        weather_sensors.mutate(
            ASCENDER_ID=ibis.literal(None, type=str),
            ROUTE_ID=ibis.literal(None, type=str),
        )
    )

    return weather