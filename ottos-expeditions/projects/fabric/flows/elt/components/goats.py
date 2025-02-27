from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("ascenders"),
        ref("routes"),
    ]
)
def goats(
    ascenders,
    routes,
    context,
):
    return ascenders.sample(0.01)
