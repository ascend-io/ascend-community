import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("alias_ascenders")])
def ascenders_analytics(
    alias_ascenders: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    ascenders_analytics = alias_ascenders
    return ascenders_analytics
