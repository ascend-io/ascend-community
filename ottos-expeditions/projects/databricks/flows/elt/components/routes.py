import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_routes")])
def routes(read_routes: ibis.Table, context: ComponentExecutionContext) -> ibis.Table:
    routes = T.clean(read_routes)
    return routes
