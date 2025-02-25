from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("ascenders"),
        ref("routes"),
        ref("telemetry"),
    ]
)
def goats(
    ascenders,
    routes,
    telemetry,
    context,
):
    return ascenders.sample(0.01)
