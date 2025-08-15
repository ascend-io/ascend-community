import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("stores"),
        ref("warehouses"),
    ]
)
def staff(
    stores: ibis.Table,
    warehouses: ibis.Table,
    context: ComponentExecutionContext,
) -> ibis.Table:
    staff = (
        stores.select(contact="owner")
        .union(warehouses.select(contact="owner"))
        .distinct(on="contact")
    )

    return staff
