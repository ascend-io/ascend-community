import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(inputs=[ref("read_telemetry_guides", flow="extract-load-databricks")])
def telemetry_guides(
    read_telemetry_guides: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    telemetry_guides = T.clean(read_telemetry_guides)
    return telemetry_guides
