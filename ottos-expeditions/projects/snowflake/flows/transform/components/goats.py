import snowflake.snowpark as sp

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(
    inputs=[
        ref("ascenders"),
        ref("routes"),
        ref("telemetry"),
    ]
)
def goats(
    ascenders: sp.Table,
    routes: sp.Table,
    telemetry: sp.Table,
    context: ComponentExecutionContext,
) -> sp.Table:
    return ascenders.sample(0.01)