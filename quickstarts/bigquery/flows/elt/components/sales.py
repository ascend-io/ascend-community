from ascend.resources import ref, transform


# TODO: add stg_store_sales and int_store_sales upstream after bugfix
@transform(
    inputs=[
        ref("int_website_sales"),
    ]
)
def sales(int_website_sales, context):
    sales = int_website_sales
    return sales
