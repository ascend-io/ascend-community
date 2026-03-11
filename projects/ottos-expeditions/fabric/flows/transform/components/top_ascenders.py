import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("ascenders"),
        ref("routes"),
        ref("telemetry"),
    ]
)
def top_ascenders(
    ascenders: ibis.Table,
    routes: ibis.Table,
    telemetry: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    if ibis.get_backend(ascenders).name == "mssql":
        n = ascenders.count().execute()
        return ascenders.limit(max(1, int(n * 0.01)))
    return ascenders.sample(0.01)
