import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_sales_vendors")])
def sales_vendors(
    read_sales_vendors: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    sales_vendors = T.clean(read_sales_vendors)
    return sales_vendors
