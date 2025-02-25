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