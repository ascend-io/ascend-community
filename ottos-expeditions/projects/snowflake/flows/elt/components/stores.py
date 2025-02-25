import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_stores")])
def stores(read_stores: ibis.Table, context) -> ibis.Table:
    stores = read_stores.distinct()
    return stores