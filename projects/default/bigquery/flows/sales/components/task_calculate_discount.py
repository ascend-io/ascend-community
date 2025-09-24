from typing import Any

import polars as pl
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("sales"),
    ]
)
def task_calculate_discount(
    sales: Any,
    context: ComponentExecutionContext,
) -> None:
    # Convert to Polars DataFrame if not already
    if not isinstance(sales, pl.DataFrame):
        try:
            sales = pl.from_pandas(sales)
        except Exception:
            sales = pl.DataFrame(sales)

    # Handle column name casing - BigQuery uses lowercase
    ascender_col = "ascender_id"
    timestamp_col = "timestamp"
    price_col = "price"

    # Select only the necessary columns and ensure proper types
    sales = sales.select([ascender_col, timestamp_col, price_col]).filter(
        pl.col(ascender_col).is_not_null()  # Filter out rows without ascender_id
    )

    # Sort by ascender_id and timestamp
    sales = sales.sort([ascender_col, timestamp_col])

    # Identify first purchase per user
    sales = sales.with_columns(
        [
            (
                pl.col(timestamp_col) == pl.col(timestamp_col).min().over(ascender_col)
            ).alias("is_first_purchase")
        ]
    )

    # Calculate discount columns
    sales = sales.with_columns(
        [
            pl.when(pl.col("is_first_purchase"))
            .then(pl.col(price_col) * 0.10)
            .otherwise(0.0)
            .alias("discount_dollars"),
        ]
    )
    sales = sales.with_columns(
        [
            (pl.col("discount_dollars") * 100).cast(pl.Int64).alias("discount_cents"),
            (pl.col(price_col) - pl.col("discount_dollars")).alias("final_price"),
        ]
    )

    # Log a sample of the output for debugging
    log("Sample of calculated discounts:")
    log(sales.head(10).to_pandas().to_string())
