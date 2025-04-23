import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_weather_sensors", flow="extract-load-databricks")])
def weather_sensors(
    read_weather_sensors: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    weather_sensors = T.clean(read_weather_sensors)
    return weather_sensors
