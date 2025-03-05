import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_weather_sensors")])
def weather_sensors(
    read_weather_sensors: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    weather_sensors = T.clean(read_weather_sensors)
    return weather_sensors
