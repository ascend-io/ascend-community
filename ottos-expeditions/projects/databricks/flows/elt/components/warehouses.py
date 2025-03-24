import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_warehouses")])
def warehouses(
    read_warehouses: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    warehouses = T.clean(read_warehouses)
    return warehouses
