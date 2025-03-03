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
        sales_stores.mutate(vendor_id=ibis.literal(None, type=str))
        .union(
            sales_website.mutate(
                vendor_id=ibis.literal(None, type=str),
                store_id=ibis.literal(0, type=str),
            )
        )
        .union(
            sales_vendors.mutate(
                store_id=ibis.literal(0, type=str),
                ascender_id=ibis.literal(None, type=str),
            )
        )
    )

    return sales
