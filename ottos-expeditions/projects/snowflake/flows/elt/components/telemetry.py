import snowflake

from ascend.resources import ref, snowpark
from ascend.context import ComponentExecutionContext


@snowpark(
    inputs=[
        ref("telemetry_guides"),
        ref("telemetry_ascenders"),
    ]
)
def telemetry(
    telemetry_guides: snowflake.snowpark.Table,
    telemetry_ascenders: snowflake.snowpark.Table,
    context: ComponentExecutionContext,
) -> snowflake.snowpark.Table:
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
