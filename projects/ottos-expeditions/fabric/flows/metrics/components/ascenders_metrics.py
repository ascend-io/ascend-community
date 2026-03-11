import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders", flow="transform")])
def ascenders_metrics(
    ascenders: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    n = ascenders.count().execute()
    return ascenders.limit(max(1, int(n * 0.1)))
