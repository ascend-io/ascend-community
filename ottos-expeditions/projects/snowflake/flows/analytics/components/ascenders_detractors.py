from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders_analytics")])
def ascenders_detractors(
    ascenders_analytics,
    context,
):
    return ascenders_analytics.sample(0.1)
