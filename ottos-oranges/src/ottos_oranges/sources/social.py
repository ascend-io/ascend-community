import ibis

import ibis.expr.datatypes as dt

from faker import Faker
from collections import OrderedDict

from ottos_oranges.sources.common import seed

social_sources = OrderedDict(
    {
        "twitter": 0.5,
        "metabook": 0.3,
        "inlinked": 0.1,
        "metagram": 0.1,
    }
)


def social_events():
    t = seed(lookback_days=7, n_uuid_cols=1, n_random_cols=3)

    faker = Faker()

    @ibis.udf.scalar.python
    def fake_row(
        timestamp: dt.timestamp,
    ) -> dt.Struct(
        {
            "source": dt.string,
        }
    ):
        """
        Generate records of fake data.
        """
        res = {
            "source": faker.random_element(social_sources),
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
