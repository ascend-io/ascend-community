from ascend.resources import ref, transform


@transform(inputs=[ref("elt_ascenders", flow="elt")])
def ascenders_analytics_v2(elt_ascenders, context):
    ascenders_analytics = elt_ascenders
    return ascenders_analytics
