from ascend.resources import ref, transform


@transform(inputs=[ref("alias_ascenders")])
def analytics_ascenders(alias_ascenders, context):
    # add your Transform logic here
    return alias_ascenders
