from ascend.resources import ref, transform


@transform(inputs=[ref("stg_inlinked")])
def int_inlinked(stg_inlinked, context):
    int_inlinked = stg_inlinked
    return int_inlinked
