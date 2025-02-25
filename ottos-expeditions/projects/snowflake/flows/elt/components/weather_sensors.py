import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_weather_sensors")])
def weather_sensors(read_weather_sensors: ibis.Table, context) -> ibis.Table:
    weather_sensors = read_weather_sensors.distinct()
    return weather_sensors