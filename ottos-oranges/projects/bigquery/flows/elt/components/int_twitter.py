from ascend.resources import ref, transform


@transform(inputs=[ref("stg_twitter")])
def int_twitter(stg_twitter, context):
    int_twitter = stg_twitter
    int_twitter = int_twitter.rename("snake_case")
    int_twitter = int_twitter.distinct()
    return int_twitter
