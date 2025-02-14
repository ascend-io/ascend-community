from ascend.resources import ref, transform


@transform(inputs=[ref("stg_email")])
def int_email(stg_email, context):
    return stg_email
