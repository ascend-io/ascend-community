from ascend.resources import ref, transform


@transform(inputs=[ref("stg_twitter")])
def int_twitter(stg_twitter, context):
    int_twitter = stg_twitter
    return int_twitter
