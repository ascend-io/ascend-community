import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_weather_routes")])
def weather_routes(read_weather_routes: ibis.Table, context) -> ibis.Table:
    weather_routes = read_weather_routes.distinct()
    return weather_routes