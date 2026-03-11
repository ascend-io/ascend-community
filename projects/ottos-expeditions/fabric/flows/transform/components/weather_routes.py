import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_weather_routes", flow="extract-load")])
def weather_routes(
    read_weather_routes: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    weather_routes = T.clean(read_weather_routes)
    return weather_routes
