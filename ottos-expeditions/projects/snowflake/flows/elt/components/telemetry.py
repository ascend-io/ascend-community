from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("telemetry_guides"),
        ref("telemetry_ascenders"),
    ]
)
def telemetry(
    telemetry_guides,
    telemetry_ascenders,
    context,
):
    telemetry = (
        telemetry_guides.rename(PERSON_ID="guide_id")
        .mutate(IS_GUIDE=True, IS_ASCENDER=False)
        .union(
            telemetry_ascenders.rename(PERSON_ID="ascender_id").mutate(
                IS_GUIDE=False, IS_ASCENDER=True
            )
        )
    )

    return telemetry