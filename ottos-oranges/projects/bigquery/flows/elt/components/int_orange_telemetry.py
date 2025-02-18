from ascend.resources import ref, transform


@transform(inputs=[ref("stg_orange_telemetry")])
def int_orange_telemetry(stg_orange_telemetry, context):
    int_orange_telemetry = stg_orange_telemetry
    int_orange_telemetry = int_orange_telemetry.rename("snake_case")
    return int_orange_telemetry
