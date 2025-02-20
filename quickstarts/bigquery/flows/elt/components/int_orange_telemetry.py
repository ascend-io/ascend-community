from ascend.resources import ref, transform


@transform(inputs=[ref("stg_orange_telemetry")])
def int_orange_telemetry(stg_orange_telemetry, context):
    int_orange_telemetry = stg_orange_telemetry
    int_orange_telemetry = int_orange_telemetry.rename("snake_case")
    int_orange_telemetry = int_orange_telemetry.distinct()
    return int_orange_telemetry
