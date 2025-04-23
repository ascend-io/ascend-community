import ibis
import ottos_expeditions.lib.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_route_closures", flow="extract-load-bigquery")])
def route_closures(
    read_route_closures: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    route_closures = T.clean(read_route_closures)
    return route_closures
