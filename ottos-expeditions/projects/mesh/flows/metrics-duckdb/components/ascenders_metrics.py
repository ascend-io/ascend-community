import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("ascenders", flow="transform-duckdb")])
def ascenders_metrics(
    ascenders: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    ascenders_metrics = ascenders.sample(0.1)
    return ascenders_metrics
