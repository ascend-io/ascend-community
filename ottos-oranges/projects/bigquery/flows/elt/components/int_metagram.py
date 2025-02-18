from ascend.resources import ref, transform


@transform(inputs=[ref("stg_metagram")])
def int_metagram(stg_metagram, context):
    int_metagram = stg_metagram
    int_metagram = int_metagram.rename("snake_case")
    return int_metagram
