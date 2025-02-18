from ascend.resources import ref, transform


@transform(inputs=[ref("stg_website_feedback")])
def int_website_feedback(stg_website_feedback, context):
    int_website_feedback = stg_website_feedback
    return int_website_feedback
