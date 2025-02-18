from ascend.resources import ref, transform


@transform(inputs=[ref("seed_orange_warehouses")])
def int_orange_warehouses(seed_orange_warehouses, context):
    int_orange_warehouses = seed_orange_warehouses
    return int_orange_warehouses
