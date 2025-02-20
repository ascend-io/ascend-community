import ibis

from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("int_store_feedback"),
        ref("int_website_feedback"),
    ]
)
def feedback(int_store_feedback, int_website_feedback, context):
    feedback = int_store_feedback.mutate(
        store_id=ibis._["store_id"].cast(int),
        timestamp=ibis._["timestamp"].cast("timestamp"),
    ).union(
        int_website_feedback.mutate(
            store_id=ibis._["store_id"].cast(int),
            timestamp=ibis._["timestamp"].cast("timestamp"),
        )
    )
    return feedback
