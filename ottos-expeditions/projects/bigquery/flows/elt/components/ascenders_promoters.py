from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders")])
def ascenders_promoters(
    ascenders,
    context,
):
    return ascenders.sample(frac=0.6)
