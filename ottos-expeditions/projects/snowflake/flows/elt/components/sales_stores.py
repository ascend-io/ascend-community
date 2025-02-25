import ibis

from ascend.resources import ref, transform, test


@transform(
    inputs=[ref("read_sales_stores")],
    materialized="table",
    tests=[test("not_null", column="TIMESTAMP")],
)
def sales_stores(read_sales_stores: ibis.Table, context) -> ibis.Table:
    sales_stores = read_sales_stores.distinct()
    return sales_stores