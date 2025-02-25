from ascend.resources import ref, transform


@transform(inputs=[ref("ascenders_alias")])
def analytics_ascenders(ascenders_alias, context):
    # add your Transform logic here
    return ascenders_alias
