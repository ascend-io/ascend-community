import ibis
import local_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_telemetry_guides")])
def telemetry_guides(
    read_telemetry_guides: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    telemetry_guides = T.clean(read_telemetry_guides)
    return telemetry_guides
