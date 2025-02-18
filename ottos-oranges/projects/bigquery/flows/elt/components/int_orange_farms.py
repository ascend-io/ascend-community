from ascend.resources import ref, transform


@transform(inputs=[ref("seed_orange_farms")])
def int_orange_farms(seed_orange_farms, context):
    int_orange_farms = seed_orange_farms
    return int_orange_farms
