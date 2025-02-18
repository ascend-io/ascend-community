from ascend.resources import ref, transform


@transform(inputs=[ref("stg_store_feedback")])
def int_store_feedback(stg_store_feedback, context):
    int_store_feedback = stg_store_feedback
    return int_store_feedback
