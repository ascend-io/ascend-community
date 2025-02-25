import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_route_closures")])
def route_closures(read_route_closures: ibis.Table, context) -> ibis.Table:
    route_closures = read_route_closures.distinct()
    return route_closures