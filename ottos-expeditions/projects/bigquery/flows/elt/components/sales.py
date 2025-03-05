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
