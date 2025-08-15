import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_stores", flow="extract-load")])
def stores(read_stores: ibis.Table, context: ComponentExecutionContext) -> ibis.Table:
    stores = T.clean(read_stores)
    return stores
