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
        stores.select(contact="owner")
        .union(warehouses.select(contact="owner"))
        .distinct(on="contact")
    )

    return staff
