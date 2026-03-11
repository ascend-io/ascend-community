import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_telemetry_guides", flow="extract-load")])
def telemetry_guides(
    read_telemetry_guides: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    telemetry_guides = T.clean(read_telemetry_guides)
    return telemetry_guides
