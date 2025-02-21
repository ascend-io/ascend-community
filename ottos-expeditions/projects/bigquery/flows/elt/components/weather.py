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
    weather = weather_routes.mutate(location=None).union(
        weather_sensors.mutate(ascender_id=None, route_id=None)
    )

    return weather
