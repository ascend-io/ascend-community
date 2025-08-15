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
        telemetry_guides.rename(person_id="guide_id")
        .mutate(is_guide=True, is_ascender=False)
        .union(
            telemetry_ascenders.rename(person_id="ascender_id").mutate(
                is_guide=False, is_ascender=True
            )
        )
    )

    return telemetry
