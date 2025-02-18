from ascend.resources import ref, transform


@transform(inputs=[ref("stg_website_sales")])
def int_website_sales(stg_website_sales, context):
    int_website_sales = stg_website_sales
    int_website_sales = int_website_sales.rename("snake_case")
    int_website_sales = int_website_sales.distinct()
    return int_website_sales
