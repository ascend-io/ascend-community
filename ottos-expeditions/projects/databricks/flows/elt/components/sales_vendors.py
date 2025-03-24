import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_sales_vendors")])
def sales_vendors(
    read_sales_vendors: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    sales_vendors = T.clean(read_sales_vendors)
    return sales_vendors
