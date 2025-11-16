from pathlib import Path

import polars as pl
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import read, test


@read(
    tests=[
        test("count_equal", count=150),
        test("not_null", column="id"),
        test("unique", column="id"),
        test("not_null", column="name"),
        test("not_null", column="breed"),
        test("not_null", column="age"),
        test("greater_than", column="age", value=0),
        test("not_null", column="route"),
    ],
    on_schema_change="sync_all_columns",
)
def read_goats_python(context: ComponentExecutionContext) -> pl.DataFrame:
    """
    Read goats data directly from the filesystem using Polars.

    Args:
        context (ComponentExecutionContext): The execution context

    Returns:
        pl.DataFrame: A Polars DataFrame containing the goats data
    """
    # Get the project path from context and construct the file path
    file_path = context.project_path / "data" / "goats.csv"

    log(f"Reading goats data from: {file_path}")

    # Read the CSV file using Polars
    df = pl.read_csv(file_path)

    log(f"Successfully read {len(df)} rows of goat data")

    return df
