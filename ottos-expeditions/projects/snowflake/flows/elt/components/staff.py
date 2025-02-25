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
        stores.select(CONTACT="owner")
        .union(warehouses.select(CONTACT="owner"))
        .distinct(on="CONTACT")
    )

    return staff