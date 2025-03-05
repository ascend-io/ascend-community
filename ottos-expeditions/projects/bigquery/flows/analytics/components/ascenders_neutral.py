import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("ascenders_analytics")])
def ascenders_neutral(
    ascenders_analytics: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    return ascenders_analytics.sample(0.3)
