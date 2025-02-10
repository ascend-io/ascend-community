import ibis
import ibis.expr.datatypes as dt

from faker import Faker
from datetime import datetime, timedelta


def seed(lookback_days: int = 365, interval_seconds: int = 60):
    lookback = ibis.interval(days=lookback_days)
    step = ibis.interval(seconds=interval_seconds)

    t = (
        (
            ibis.range(
                ibis.now() - lookback,
                ibis.now(),
                step=step,
            )
            .unnest()
            .name("timestamp")
            .as_table()
        )
        .mutate(
            index=(ibis.row_number().over(order_by="timestamp")),
            **{col: 2 * (ibis.random() - 0.5) for col in ["a", "b", "c"]},
        )
        .mutate(color=ibis._["index"].histogram(nbins=8))
        .drop("index")
        .relocate("timestamp", "color")
        .order_by("timestamp")
    )

    return t


def walk(seed):
    window = ibis.window(order_by="timestamp", preceding=None, following=0)
    walked = seed.select(
        "timestamp",
        "color",
        a=seed["a"].sum().over(window),
        b=seed["b"].sum().over(window),
        c=seed["c"].sum().over(window),
    ).order_by("timestamp")

    return walked


def fake(walk):
    faker = Faker()

    record_schema = dt.Struct(
        {
            "timestamp": datetime,
            "name": str,
            "comment": str,
            "location": list[str],
            "device": dt.Struct(
                {
                    "browser": str,
                    "ip": str,
                }
            ),
        }
    )

    @ibis.udf.scalar.python
    def faked_batch(
        timestamp: datetime,
        a: float,
        b: float,
        c: float,
        batch_size: int = 8,
    ) -> dt.Array(record_schema):
        """
        Generate records of fake data.
        """
        value = (a + b + c) / 3

        res = [
            {
                "timestamp": timestamp + timedelta(seconds=0.1 * i),
                "name": faker.name() if value >= 0.5 else faker.first_name(),
                "comment": faker.sentence(),
                "location": faker.location_on_land(),
                "device": {
                    "browser": faker.user_agent(),
                    "ip": faker.ipv4() if value >= 0 else faker.ipv6(),
                },
            }
            for i in range(batch_size)
        ]

        return res

    faked = (
        walk.mutate(
            faked=faked_batch(walk["timestamp"], walk["a"], walk["b"], walk["c"]),
        )
        .select(
            "a",
            "b",
            "c",
            ibis._["faked"].unnest(),
        )
        .unpack("faked")
        .drop("a", "b", "c")
    )

    return faked
