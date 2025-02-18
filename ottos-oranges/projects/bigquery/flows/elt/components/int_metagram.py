from ascend.resources import ref, transform


@transform(inputs=[ref("stg_metagram")])
def int_metagram(stg_metagram, context):
    int_metagram = stg_metagram
    return int_metagram
