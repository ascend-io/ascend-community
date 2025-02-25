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
        stores.select(CONTACT="OWNER")
        .union(warehouses.select(CONTACT="OWNER"))
        .distinct(on="CONTACT")
    )

    return staff
