import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_weather_routes")])
def weather_routes(
    read_weather_routes: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    weather_routes = T.clean(read_weather_routes)
    return weather_routes
