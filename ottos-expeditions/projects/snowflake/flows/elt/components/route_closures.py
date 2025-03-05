import ibis

import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_route_closures")])
def route_closures(read_route_closures: ibis.Table, context) -> ibis.Table:
    route_closures = T.clean(read_route_closures)
    return route_closures
