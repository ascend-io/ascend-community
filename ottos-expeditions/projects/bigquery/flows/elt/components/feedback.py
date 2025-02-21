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
    feedback = feedback_ascenders.union(feedback_stores).union(feedback_website)

    return feedback
