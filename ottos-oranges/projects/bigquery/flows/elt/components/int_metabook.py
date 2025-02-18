from ascend.resources import ref, transform


@transform(inputs=[ref("stg_metabook")])
def int_metabook(stg_metabook, context):
    int_metabook = stg_metabook
    int_metabook = int_metabook.rename("snake_case")
    return int_metabook
