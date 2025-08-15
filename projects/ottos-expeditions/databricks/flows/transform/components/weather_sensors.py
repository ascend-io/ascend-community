import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_weather_sensors", flow="extract-load")])
def weather_sensors(
    read_weather_sensors: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    weather_sensors = T.clean(read_weather_sensors)
    return weather_sensors
