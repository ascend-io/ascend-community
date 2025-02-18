from ascend.resources import ref, transform


@transform(inputs=[ref("seed_orange_stores")])
def int_orange_stores(seed_orange_stores, context):
    int_orange_stores = seed_orange_stores
    return int_orange_stores
