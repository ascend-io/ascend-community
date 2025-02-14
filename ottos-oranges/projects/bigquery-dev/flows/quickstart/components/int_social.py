from ascend.resources import ref, transform


@transform(inputs=[ref("stg_social")])
def int_social(stg_social, context):
    return stg_social
