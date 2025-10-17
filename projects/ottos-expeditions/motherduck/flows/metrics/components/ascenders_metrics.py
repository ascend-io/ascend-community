import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders", flow="transform")])
def ascenders_metrics(
    ascenders: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    ascenders_metrics = ascenders.sample(0.1)
    return ascenders_metrics
