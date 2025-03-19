import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_guides")])
def guides(read_guides: ibis.Table, context: ComponentExecutionContext) -> ibis.Table:
    guides = T.clean(read_guides)
    return guides
