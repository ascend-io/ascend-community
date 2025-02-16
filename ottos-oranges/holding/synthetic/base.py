# imports
import os
import ibis

from ottos_oranges.lib.synthetic.seed import orange_stores, orange_types
from ottos_oranges.lib.synthetic.common import ts, BASE_DIR


# functions
def oranges(overwrite: bool = False) -> ibis.Table:
    # check if the data exists
    filename = "oranges.parquet"
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.exists(filepath) or overwrite:
        t = ts(lookback_days=113, interval_seconds=1)
        t = t.mutate(index=ibis.row_number())
        t = t.drop("timestamp")
        t = t.cross_join(orange_types())
        t = t.rename("snake_case")
        t = t.drop("index")
        t = t.drop("description")
        t = t.mutate(id=ibis.uuid().cast(str))
        t = t.relocate("id")
        t = t.select("id", "orange_sku")

        t.to_parquet(filepath, partition_by=("orange_sku"), overwrite=overwrite)

    return ibis.read_parquet(
        os.path.join(filepath, "orange_sku=*", "*.parquet"), hive_partitioning=True
    ).relocate("id", "orange_sku")


def orange_prices(overwrite: bool = False) -> ibis.Table:
    # check if the data exists
    filename = "orange_prices.csv"
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.exists(filepath) or overwrite:
        t = orange_stores().cross_join(orange_types())
        t = t.mutate(price_per_oz=((0.5 + ibis.random()) * 1.3))
        t = t.mutate(price_per_oz=ibis._["price_per_oz"].round(2))
        t = t.rename("snake_case")
        t = t.select("store_id", "orange_sku", "price_per_oz")
        t = t.order_by(ibis.desc("price_per_oz"), "orange_sku")

        t.to_csv(filepath, overwrite=overwrite)

    return ibis.read_csv(filepath)
