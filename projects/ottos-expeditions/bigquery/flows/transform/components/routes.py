import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_routes", flow="extract-load")])
def routes(read_routes: ibis.Table, context: ComponentExecutionContext) -> ibis.Table:
    routes = T.clean(read_routes)
    return routes
