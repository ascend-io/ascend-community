import ibis

from ascend.resources import ref, transform
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref("sales_stores"),
        ref("sales_website"),
        ref("sales_vendors"),
    ]
)
def sales(
    sales_stores: ibis.Table,
    sales_website: ibis.Table,
    sales_vendors: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
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
