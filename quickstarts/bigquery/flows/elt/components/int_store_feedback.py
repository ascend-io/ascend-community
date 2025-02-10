from ascend.resources import ref, transform


@transform(inputs=[ref("stg_store_feedback")])
def int_store_feedback(stg_store_feedback, context):
    int_store_feedback = stg_store_feedback
    int_store_feedback = int_store_feedback.rename("snake_case")
    return int_store_feedback
