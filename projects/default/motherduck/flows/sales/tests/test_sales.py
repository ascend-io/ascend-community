from ascend.resources import TestResult, ref, singular_test


@singular_test(
    inputs=[
        ref("sales_website"),
        ref("sales_stores"),
        ref("sales_vendors"),
    ],
    severity="error",
)
def test_sales(context, sales_website, sales_stores, sales_vendors):
    stores_count = sales_stores.count().execute()
    vendors_count = sales_vendors.count().execute()
    website_count = sales_website.count().execute()

    # Use an empty Ibis table with the same schema as sales_stores for all test results
    empty_table = sales_stores.limit(0)

    if stores_count > 0:
        yield TestResult(
            "sales_stores_validation",
            True,
            empty_table,
            f"sales_stores has {stores_count} rows",
        )
    else:
        yield TestResult(
            "sales_stores_validation", False, empty_table, "sales_stores is empty"
        )

    if vendors_count > 0:
        yield TestResult(
            "sales_vendors_validation",
            True,
            empty_table,
            f"sales_vendors has {vendors_count} rows",
        )
    else:
        yield TestResult(
            "sales_vendors_validation", False, empty_table, "sales_vendors is empty"
        )

    if website_count > 0:
        yield TestResult(
            "sales_website_validation",
            True,
            empty_table,
            f"sales_website has {website_count} rows",
        )
    else:
        yield TestResult(
            "sales_website_validation", False, empty_table, "sales_website is empty"
        )
