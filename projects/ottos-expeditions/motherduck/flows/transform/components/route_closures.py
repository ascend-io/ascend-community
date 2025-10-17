import ibis
import ottos_expeditions.lib.transform as T
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_route_closures", flow="extract-load")])
def route_closures(
    read_route_closures: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    route_closures = T.clean(read_route_closures)
    return route_closures
