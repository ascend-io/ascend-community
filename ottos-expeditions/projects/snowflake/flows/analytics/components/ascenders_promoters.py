from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders_alias")])
def ascenders_promoters(
    ascenders_alias,
    context,
):
    return ascenders_alias.sample(0.6)
