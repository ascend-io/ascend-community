from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders")])
def ascenders_neutral(
    ascenders,
    context,
):
    return ascenders.sample(frac=0.3)
