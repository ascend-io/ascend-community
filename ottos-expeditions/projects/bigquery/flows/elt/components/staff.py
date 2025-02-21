from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("stores"),
        ref("warehouses"),
    ]
)
def staff(
    stores,
    warehouses,
    context,
):
    staff = (
        stores.select(contact="store_owner")
        .union(warehouses.select(contact="warehouse_owner"))
        .distinct(on="contact")
    )

    return staff
