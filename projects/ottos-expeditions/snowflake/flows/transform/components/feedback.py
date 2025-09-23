import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, test, transform


@transform(
    inputs=[
        ref("feedback_ascenders"),
        ref("feedback_stores"),
        ref("feedback_website"),
    ],
    tests=[
        test("not_null", column="ID", severity="error"),
        test("count_greater_than", count=0, severity="error"),
    ],
)
def feedback(
    feedback_ascenders: ibis.Table,
    feedback_stores: ibis.Table,
    feedback_website: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    feedback = (
        feedback_ascenders.drop("RAW_URI", "INGESTED_AT")
        .mutate(
            STORE_ID=ibis.literal(None, type=str), USER_ID=ibis.literal(None, type=str)
        )
        .union(
            feedback_stores.mutate(
                ASCENDER_ID=ibis.literal(None, type=str),
                USER_ID=ibis.literal(None, type=str),
                STORE_ID=ibis._["STORE_ID"].cast("string"),
            )
        )
        .union(
            feedback_website.mutate(
                FEEDBACK=ibis.literal(None, type=str),
                ASCENDER_ID=ibis.literal(None, type=str),
                STORE_ID=ibis.literal("website", type=str),
            )
        )
    )

    return feedback
