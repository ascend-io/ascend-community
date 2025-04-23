import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_routes", flow="extract-load-databricks")])
def routes(read_routes: ibis.Table, context: ComponentExecutionContext) -> ibis.Table:
    routes = T.clean(read_routes)
    return routes
