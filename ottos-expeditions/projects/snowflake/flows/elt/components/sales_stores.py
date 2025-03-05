import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark, test
from ascend.application.context import ComponentExecutionContext


@snowpark(
    inputs=[ref("read_sales_stores")],
    materialized="table",
    tests=[test("not_null", column="TIMESTAMP")],
)
def sales_stores(
    read_sales_stores: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    sales_stores = T.clean(read_sales_stores)
    return sales_stores
