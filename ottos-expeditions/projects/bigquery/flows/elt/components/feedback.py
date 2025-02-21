import ibis

from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("feedback_ascenders"),
        ref("feedback_stores"),
        ref("feedback_website"),
    ]
)
def feedback(
    feedback_ascenders,
    feedback_stores,
    feedback_website,
    context,
):
    feedback = (
        feedback_ascenders.mutate(
            store_id=ibis.literal(None, type=str), user_id=ibis.literal(None, type=str)
        )
        .union(
            feedback_stores.mutate(
                ascender_id=ibis.literal(None, type=str),
                user_id=ibis.literal(None, type=str),
            )
        )
        .union(
            feedback_website.mutate(
                ascender_id=ibis.literal(None, type=str),
                store_id=ibis.literal(0, type=str),
            )
        )
    )

    return feedback
