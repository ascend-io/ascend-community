import ibis

import ibis.expr.datatypes as dt

from faker import Faker
from collections import OrderedDict

from ottos_oranges.sources.common import seed

orange_types = OrderedDict(
    {
        "navel": 0.5,
        "mandarin": 0.3,
        "blood": 0.1,
        "valencia": 0.1,
    }
)


def telemetry_events():
    t = seed(lookback_days=7, n_uuid_cols=1, n_random_cols=3)

    faker = Faker()

    @ibis.udf.scalar.python
    def fake_row(
        timestamp: dt.timestamp,
    ) -> dt.Struct(
        {
            "orange_type": dt.string,
        }
    ):
        """
        Generate records of fake data.
        """
        res = {
            "orange_type": faker.random_element(orange_types),
        }

        return res

    t = (
        t.mutate(
            faked=fake_row(
                t["timestamp"],
            )
        )
        .select(
            "timestamp",
            ibis._["uuid_a"].name("event_id"),
            ibis._["faked"],
        )
        .unpack("faked")
        .order_by("timestamp")
    )

    return t
