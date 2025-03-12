import ibis
import polars as pl

# from datetime import datetime, timedelta

from ascend.resources import read
from ascend.application.context import ComponentExecutionContext
# from ascend.application.context import IncrementalComponentExecutionContext


# @read(strategy="incremental", incremental_strategy="merge", unique_key="id")
# def read_sales_stores(context: IncrementalComponentExecutionContext):
#     max_timestamp = datetime.utcnow() - timedelta(days=730)
#     if context.is_incremental:
#         current_data = context.current_data()
#         max_timestamp = current_data["timestamp"].max().to_pyarrow().as_py()
#     t = ibis.read_parquet(
#         "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/generated/events/sales_store.parquet/year=*/month=*/day=*/*.parquet"
#     )
#     t = t.filter(t["timestamp"] > max_timestamp)
#
#     return t.to_pandas()


@read()
def read_sales_stores(context: ComponentExecutionContext):
    t = ibis.read_parquet(
        "gs://ascend-io-gcs-public/ottos-expeditions/lakev0/generated/events/sales_store.parquet/year=*/month=*/day=*/*.parquet"
    )
    return t
