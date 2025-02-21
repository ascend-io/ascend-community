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
    staff,
    routes,
    guides,
    route_closures,
    telemetry,
    weather,
    sales,
    social_media,
    feedback,
    context,
):
    return telemetry
