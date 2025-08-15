import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, test, transform


@transform(
    inputs=[ref("read_sales_stores", flow="extract-load")],
    materialized="table",
    tests=[test("not_null", column="timestamp")],
)
def sales_stores(
    read_sales_stores: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    sales_stores = T.clean(read_sales_stores)
    return sales_stores
