import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_telemetry_guides")])
def telemetry_guides(read_telemetry_guides: ibis.Table, context) -> ibis.Table:
    return T.clean(read_telemetry_guides)
