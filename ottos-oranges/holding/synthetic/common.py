# imports
import os
import ibis

# configuration
LOOKBACK_DAYS = 7
INTERVAL_SECONDS = 60

LAKE_DIR = "lake"
SEED_DIR = os.path.join(LAKE_DIR, "seed")
GENERATED_DIR = os.path.join(LAKE_DIR, "generated")
BASE_DIR = os.path.join(GENERATED_DIR, "base")
EVENTS_DIR = os.path.join(GENERATED_DIR, "events")


# functions
def tn(
    n: int = None,
) -> ibis.Table:
    assert 0 < n, "n must be greater than 0"
    t = ibis.range(0, n).unnest().name("index").as_table()
    t = t.order_by("index")

    return t


def ts(
    lookback_days: int = None,
    interval_seconds: int = None,
) -> ibis.Table:
    assert 0 < lookback_days <= 3650, "lookback days must be between 1 and 3650"
    assert 0 < interval_seconds <= 3600, "interval seconds must be between 1 and 3600"
    lookback = ibis.interval(days=lookback_days)
    step = ibis.interval(seconds=interval_seconds)
    t = (
        ibis.range(
            ibis.now() - lookback,
            ibis.now(),
            step=step,
        )
        .unnest()
        .name("timestamp")
        .as_table()
    )
    t = t.order_by("timestamp")

    return t


def add_uuid_col(
    t: ibis.Table, col: str = "id", cast_to_str: bool = True
) -> ibis.Table:
    return t.mutate(**{col: ibis.uuid().cast(str) if cast_to_str else ibis.uuid()})


def add_random_col(t: ibis.Table, col: str = "rand") -> ibis.Table:
    return t.mutate(**{col: ibis.random()})


def downsample(t: ibis.Table, downsample_factor: float) -> ibis.Table:
    assert 0 < downsample_factor < 1, "downsample factor must be between 0 and 1"
    t = t.mutate(_downsample_on=ibis.random())
    t = t.filter(t["_downsample_on"] < downsample_factor)
    t = t.drop("_downsample_on")
    return t


def duplicate(t: ibis.Table, duplicate_factor: float) -> ibis.Table:
    assert 0 < duplicate_factor < 1, "duplicate factor must be between 0 and 1"
    t2 = downsample(t, duplicate_factor)
    return t.union(t2)


def walk(t: ibis.Table, walk_cols: list[str]) -> ibis.Table:
    window = ibis.window(order_by="timestamp", preceding=None, following=0)
    walked = t.mutate(**{col: t[col].sum().over(window) for col in walk_cols})
    walked = walked.relocate(t.columns).order_by("timestamp")
    return walked
