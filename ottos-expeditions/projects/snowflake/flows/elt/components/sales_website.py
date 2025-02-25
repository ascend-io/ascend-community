import ibis

from ascend.resources import ref, transform, test


@transform(
    inputs=[
        ref(
            "read_sales_website",
            reshape={"time": {"column": "TIMESTAMP", "granularity": "month"}},
        )
    ],
    materialized="table",
    tests=[test("not_null", column="TIMESTAMP")],
)
def sales_website(read_sales_website: ibis.Table, context) -> ibis.Table:
    sales_website = read_sales_website.distinct()
    return sales_website