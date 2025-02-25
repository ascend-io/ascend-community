import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_telemetry_ascenders")])
def telemetry_ascenders(read_telemetry_ascenders: ibis.Table, context) -> ibis.Table:
    telemetry_ascenders = T.clean(read_telemetry_ascenders)
    return telemetry_ascenders