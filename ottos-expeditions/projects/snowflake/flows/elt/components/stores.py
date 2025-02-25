import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_stores")])
def stores(read_stores: ibis.Table, context) -> ibis.Table:
    stores = T.clean(read_stores)
    return stores