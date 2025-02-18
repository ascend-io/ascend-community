from ascend.resources import ref, transform


@transform(inputs=[ref("stg_metabook")])
def int_metabook(stg_metabook, context):
    int_metabook = stg_metabook
    return int_metabook
