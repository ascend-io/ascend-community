import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_telemetry_ascenders")])
def telemetry_ascenders(read_telemetry_ascenders: ibis.Table, context) -> ibis.Table:
    telemetry_ascenders = read_telemetry_ascenders.distinct()
    return telemetry_ascenders