import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_routes")])
def routes(read_routes: ibis.Table, context) -> ibis.Table:
    routes = T.clean(read_routes)
    return routes
