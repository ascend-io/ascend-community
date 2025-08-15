import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_route_closures", flow="extract-load")])
def route_closures(
    read_route_closures: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    route_closures = T.clean(read_route_closures)
    return route_closures
