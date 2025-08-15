import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("telemetry_guides"),
        ref("telemetry_ascenders"),
    ]
)
def telemetry(
    telemetry_guides: ibis.Table,
    telemetry_ascenders: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    telemetry = (
        telemetry_guides.rename(PERSON_ID="GUIDE_ID")
        .mutate(IS_GUIDE=True, IS_ASCENDER=False)
        .union(
            telemetry_ascenders.rename(PERSON_ID="ASCENDER_ID").mutate(
                IS_GUIDE=False, IS_ASCENDER=True
            )
        )
    )

    return telemetry
