from ascend.resources import ref, transform


@transform(inputs=[ref("stg_website_sales")])
def int_website_sales(stg_website_sales, context):
    int_website_sales = stg_website_sales
    return int_website_sales
