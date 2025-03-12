import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("ascenders", flow="elt")])
def ascenders_analytics(
    ascenders: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    ascenders_analytics = ascenders
    return ascenders_analytics
