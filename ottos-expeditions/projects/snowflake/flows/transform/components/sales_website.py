import ibis
import ascend_project_code.transform as T

from ascend.resources import ref, transform, test
from ascend.application.context import ComponentExecutionContext


@transform(
    inputs=[
        ref(
            "read_sales_website",
            flow="extract-load",
            reshape={"time": {"column": "timestamp", "granularity": "day"}},
        )
    ],
    materialized="table",
    tests=[test("not_null", column="timestamp")],
)
def sales_website(
    read_sales_website: ibis.Table, context: ComponentExecutionContext
) -> ibis.Table:
    sales_website = T.clean(read_sales_website)
    return sales_website
