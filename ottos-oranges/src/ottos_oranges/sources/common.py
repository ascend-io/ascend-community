import ibis

from string import ascii_lowercase


def seed(
    lookback_days: int = 365,
    interval_seconds: int = 60,
    n_uuid_cols: int = 0,
    n_random_cols: int = 3,
):
    """Generate seed data."""

    assert 0 < lookback_days <= 3650, "Lookback days must be between 1 and 3650"
    assert 0 < interval_seconds <= 3600, "Interval seconds must be between 1 and 3600"
    assert 0 <= n_uuid_cols <= 26, "Maximum of 26 UUID columns"
    assert 0 <= n_random_cols <= 26, "Maximum of 26 random columns"

    lookback = ibis.interval(days=lookback_days)
    step = ibis.interval(seconds=interval_seconds)

    uuid_cols = [f"uuid_{x}" for x in list(ascii_lowercase[:n_uuid_cols])]
    random_cols = [f"rand_{x}" for x in list(ascii_lowercase[:n_random_cols])]

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

    uuid_dict = {col: ibis.uuid() for col in uuid_cols}
    if uuid_dict:
        t = t.mutate(**uuid_dict)

    random_dict = {col: 2 * (ibis.random() - 0.5) for col in random_cols}
    if random_dict:
        t = t.mutate(**random_dict)

    t = t.order_by("timestamp")

    return t


def walk(t, walk_cols: list[str]):
    """Replace random numbers with a random walk."""

    window = ibis.window(order_by="timestamp", preceding=None, following=0)
    walked = t.mutate(**{col: t[col].sum().over(window) for col in walk_cols})
    walked = walked.relocate(t.columns).order_by("timestamp")

    return walked
