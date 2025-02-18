from ascend.resources import ref, transform


@transform(inputs=[ref("seed_orange_farms")])
def int_orange_farms(seed_orange_farms, context):
    int_orange_farms = seed_orange_farms
    int_orange_farms = int_orange_farms.rename("snake_case")
    int_orange_farms = int_orange_farms.distinct()
    return int_orange_farms
