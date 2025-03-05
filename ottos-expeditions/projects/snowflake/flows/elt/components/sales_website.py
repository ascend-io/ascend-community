import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark, test
from ascend.application.context import ComponentExecutionContext


@snowpark(
    inputs=[
        ref(
            "read_sales_website",
            reshape={"time": {"column": "TIMESTAMP", "granularity": "month"}},
        )
    ],
    materialized="table",
    tests=[test("not_null", column="TIMESTAMP")],
)
def sales_website(
    read_sales_website: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    sales_website = T.clean(read_sales_website)
    return sales_website
