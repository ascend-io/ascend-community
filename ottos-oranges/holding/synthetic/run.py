import time

from rich import print

from ottos_oranges.lib.synthetic import base

# from ottos_oranges.lib.synthetic.events.email import EmailEvents
# from ottos_oranges.lib.synthetic.events.store import StoreEvents
# from ottos_oranges.lib.synthetic.events.social import SocialEvents
# from ottos_oranges.lib.synthetic.events.website import WebsiteEvents
# from ottos_oranges.lib.synthetic.events.telemetry import TelemetryEvents


def run_simulation(
    lookback_days: int = None,
    interval_seconds: int = None,
):
    print()
    print("oranges:")
    start = time.time()
    t = base.oranges()
    print(t.schema())
    print(t.preview())
    print(f"rows: {t.count().to_pyarrow().as_py():,}")
    print(f"columns: {len(t.columns):,}")
    end = time.time()
    print(f"elapsed: {end - start:.2f}s")

    print()
    print("orange_prices:")
    start = time.time()
    t = base.orange_prices()
    print(t.schema())
    print(t.preview())
    print(f"rows: {t.count().to_pyarrow().as_py():,}")
    print(f"columns: {len(t.columns):,}")
    end = time.time()
    print(f"elapsed: {end - start:.2f}s")


# def run_simulation(
#     lookback_days: int = None,
#     interval_seconds: int = None,
# ):
#     # generate all the tables
#     tbls = [
#         EmailEvents,
#         StoreEvents,
#         SocialEvents,
#         WebsiteEvents,
#         TelemetryEvents,
#     ]
#     for T in tbls:
#         print()
#         print(f"\t{T.__name__}:")
#         start = time.time()
#         tbl = T(lookback_days=lookback_days, interval_seconds=interval_seconds)
#         print(tbl.t.schema())
#         print(tbl.t.preview())
#         print(f"rows: {tbl.t.count().to_pyarrow().as_py():,}")
#         print(f"columns: {len(tbl.t.columns):,}")
#         tbl.write()
#         end = time.time()
#         print(f"\telapsed: {end - start:.2f}s")
