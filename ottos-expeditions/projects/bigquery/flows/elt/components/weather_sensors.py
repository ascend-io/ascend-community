import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_weather_sensors")])
def weather_sensors(read_weather_sensors: ibis.Table, context) -> ibis.Table:
    return T.clean(read_weather_sensors)
