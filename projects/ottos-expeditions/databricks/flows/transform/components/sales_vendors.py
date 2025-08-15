import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_sales_vendors", flow="extract-load")])
def sales_vendors(
    read_sales_vendors: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    sales_vendors = T.clean(read_sales_vendors)
    return sales_vendors
