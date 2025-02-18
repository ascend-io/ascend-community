from ascend.resources import ref, transform


@transform(
    inputs=[
        ref("int_orange_farms"),
        ref("int_orange_stores"),
        ref("int_orange_warehouses"),
    ]
)
def staff(
    int_orange_farms,
    int_orange_stores,
    int_orange_warehouses,
    context,
):
    staff = (
        int_orange_farms.select(contact="farm_owner")
        .union(int_orange_stores.select(contact="store_owner"))
        .union(int_orange_warehouses.select(contact="warehouse_owner"))
    )

    return staff
