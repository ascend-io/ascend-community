import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_warehouses", flow="extract-load")])
def warehouses(
    read_warehouses: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    warehouses = T.clean(read_warehouses)
    return warehouses
