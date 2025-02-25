import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_routes")])
def routes(read_routes: ibis.Table, context) -> ibis.Table:
    routes = read_routes.distinct()
    return routes