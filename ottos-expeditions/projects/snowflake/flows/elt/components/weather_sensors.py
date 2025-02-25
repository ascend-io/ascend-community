import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_weather_sensors")])
def weather_sensors(read_weather_sensors: ibis.Table, context) -> ibis.Table:
    weather_sensors = T.clean(read_weather_sensors)
    return weather_sensors