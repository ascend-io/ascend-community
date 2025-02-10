from ascend.resources import transform, ref


@transform(inputs=[ref("seed")])
# TODO: ctx vs context here
def expand(seed, context):
    return seed.union(seed)
