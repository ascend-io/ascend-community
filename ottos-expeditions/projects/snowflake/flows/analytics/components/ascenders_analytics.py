from ascend.resources import ref, transform


@transform(inputs=[ref("alias_ascenders")])
def ascenders_analytics(alias_ascenders, context):
    ascenders_analytics = alias_ascenders
    return ascenders_analytics
