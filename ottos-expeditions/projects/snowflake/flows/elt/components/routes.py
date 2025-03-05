import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_routes")])
def routes(
    read_routes: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    routes = T.clean(read_routes)
    return routes
