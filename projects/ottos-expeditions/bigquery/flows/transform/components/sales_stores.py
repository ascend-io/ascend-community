import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform, test
from ascend.application.context import ComponentExecutionContext


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
