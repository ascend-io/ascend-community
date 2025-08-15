import ascend_project_code.transform as T
import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(inputs=[ref("read_telemetry_ascenders", flow="extract-load")])
def telemetry_ascenders(
    read_telemetry_ascenders: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    telemetry_ascenders = T.clean(read_telemetry_ascenders)
    return telemetry_ascenders
