from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("int_orange_farms"),
        ref("int_orange_types"),
        ref("int_orange_stores"),
        ref("int_orange_warehouses"),
        ref("int_orange_telemetry"),
        ref("sales"),
        ref("feedback"),
    ]
)
def oranges(
    int_orange_farms,
    int_orange_types,
    int_orange_stores,
    int_orange_warehouses,
    int_orange_telemetry,
    sales,
    feedback,
    context,
):
    oranges = int_orange_telemetry
    return oranges
