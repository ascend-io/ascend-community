from ascend.resources import ref, transform


@transform(inputs=[ref("stg_metabook")])
def int_metabook(stg_metabook, context):
    int_metabook = stg_metabook
    int_metabook = int_metabook.rename("snake_case")
    int_metabook = int_metabook.distinct()
    return int_metabook
