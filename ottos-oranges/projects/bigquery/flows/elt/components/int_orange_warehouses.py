from ascend.resources import ref, transform


@transform(inputs=[ref("seed_orange_warehouses")])
def int_orange_warehouses(seed_orange_warehouses, context):
    int_orange_warehouses = seed_orange_warehouses
    int_orange_warehouses = int_orange_warehouses.rename("snake_case")
    int_orange_warehouses = int_orange_warehouses.distinct()
    return int_orange_warehouses
