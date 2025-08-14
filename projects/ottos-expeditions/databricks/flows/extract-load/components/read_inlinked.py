import polars as pl
import pyarrow as pa

from ascend.resources import read
from ascend.common.events import log
from ascend.application.context import ComponentExecutionContext


@read(
    strategy="incremental",
    incremental_strategy="merge",
    unique_key="id",
    on_schema_change="sync_all_columns",
)
def read_inlinked(context: ComponentExecutionContext) -> pa.Table:
    df = pl.read_parquet(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/generated/events/inlinked.parquet/year=*/month=*/day=*/*.parquet"
    )
    current_data = context.current_data()
    if current_data is not None:
        current_data = current_data.to_polars()
        max_ts = current_data["timestamp"].max()
        log(f"Reading data after {max_ts}")
        df = df.filter(df["timestamp"] > max_ts)
    else:
        log("No current data found, loading all data")

    log(f"Returning {df.height} rows")
    return df.to_arrow()
