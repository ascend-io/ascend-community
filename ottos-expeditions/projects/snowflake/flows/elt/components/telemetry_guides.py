import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_telemetry_guides")])
def telemetry_guides(read_telemetry_guides: ibis.Table, context) -> ibis.Table:
    telemetry_guides = read_telemetry_guides.distinct()
    return telemetry_guides