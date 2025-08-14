import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("feedback_ascenders"),
        ref("feedback_stores"),
        ref("feedback_website"),
    ]
)
def feedback(
    feedback_ascenders: ibis.Table,
    feedback_stores: ibis.Table,
    feedback_website: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    feedback = (
        feedback_ascenders.drop("raw_uri", "ingested_at")
        .mutate(
            store_id=ibis.literal(None, type=str), user_id=ibis.literal(None, type=str)
        )
        .union(
            feedback_stores.mutate(
                ascender_id=ibis.literal(None, type=str),
                user_id=ibis.literal(None, type=str),
                store_id=ibis._["store_id"].cast("string"),
            )
        )
        .union(
            feedback_website.mutate(
                feedback=ibis.literal(None, type=str),
                ascender_id=ibis.literal(None, type=str),
                store_id=ibis.literal("website", type=str),
            )
        )
    )

    return feedback
