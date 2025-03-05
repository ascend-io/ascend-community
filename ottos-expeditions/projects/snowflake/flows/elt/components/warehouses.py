import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_warehouses")])
def warehouses(
    read_warehouses: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    warehouses = T.clean(read_warehouses)
    return warehouses
