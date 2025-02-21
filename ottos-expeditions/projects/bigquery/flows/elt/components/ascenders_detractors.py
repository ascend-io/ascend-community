from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders")])
def ascenders_detractors(
    ascenders,
    context,
):
    return ascenders.sample(0.1)
