from ascend.resources import ref, transform


@transform(inputs=[ref("seed_orange_types")])
def int_orange_types(seed_orange_types, context):
    int_orange_types = seed_orange_types
    return int_orange_types
