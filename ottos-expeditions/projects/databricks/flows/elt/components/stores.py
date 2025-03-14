import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_stores")])
def stores(read_stores: ibis.Table, context: ComponentExecutionContext) -> ibis.Table:
    stores = T.clean(read_stores)
    return stores
