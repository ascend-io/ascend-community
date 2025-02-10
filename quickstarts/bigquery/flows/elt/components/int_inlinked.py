from ascend.resources import ref, transform


@transform(inputs=[ref("stg_inlinked")])
def int_inlinked(stg_inlinked, context):
    int_inlinked = stg_inlinked
    int_inlinked = int_inlinked.rename("snake_case")
    int_inlinked = int_inlinked.distinct()
    return int_inlinked
