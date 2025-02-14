from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("int_social"),
        ref("int_email"),
        ref("int_website"),
        ref("int_store"),
        ref("int_telemetry"),
    ]
)
def rpt_joined(int_store, int_social, int_email, int_website, int_telemetry, context):
    return (
        int_store.join(int_social, "event_id")
        .join(int_email, "event_id")
        .join(int_website, "event_id")
        .join(int_telemetry, "event_id")
    )
