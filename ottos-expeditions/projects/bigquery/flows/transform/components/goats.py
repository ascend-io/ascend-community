import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("ascenders"),
        ref("routes"),
        ref("telemetry"),
    ]
)
def goats(
    ascenders: ibis.Table,
    routes: ibis.Table,
    telemetry: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    return ascenders.sample(0.01)
