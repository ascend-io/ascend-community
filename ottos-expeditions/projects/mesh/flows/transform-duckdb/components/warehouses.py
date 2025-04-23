import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_warehouses", flow="extract-load-duckdb")])
def warehouses(
    read_warehouses: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    warehouses = T.clean(read_warehouses)
    return warehouses
