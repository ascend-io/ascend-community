import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_weather_routes")])
def weather_routes(
    read_weather_routes: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    weather_routes = T.clean(read_weather_routes)
    return weather_routes
