import snowflake
import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_route_closures")])
def route_closures(
    read_route_closures: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    route_closures = T.clean(read_route_closures)
    return route_closures
