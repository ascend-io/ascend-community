import ibis

from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("sales_stores"),
        ref("sales_website"),
        ref("sales_vendors"),
    ]
)
def sales(
    sales_stores,
    sales_website,
    sales_vendors,
    context,
):
    sales = (
        sales_stores.mutate(VENDOR_ID=ibis.literal(None, type=str))
        .union(
            sales_website.mutate(
                VENDOR_ID=ibis.literal(None, type=str),
                STORE_ID=ibis.literal(0, type=str),
            )
        )
        .union(
            sales_vendors.mutate(
                STORE_ID=ibis.literal(0, type=str),
                ASCENDER_ID=ibis.literal(None, type=str),
            )
        )
    )

    return sales
