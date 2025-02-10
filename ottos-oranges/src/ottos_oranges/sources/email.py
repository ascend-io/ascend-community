import ibis

import ibis.expr.datatypes as dt

from faker import Faker
from collections import OrderedDict

from ottos_oranges.sources.common import seed

from_emails = OrderedDict(
    {
        "marketing@ottosoranges.ai": 0.5,
        "sales@ottosoranges.ai": 0.3,
        "hello@ottosoranges.ai": 0.2,
    }
)


def email_events():
    t = seed(lookback_days=7, n_uuid_cols=1, n_random_cols=3)

    faker = Faker()

    @ibis.udf.scalar.python
    def fake_row(
        timestamp: dt.timestamp,
        rand_a: float,
        rand_b: float,
        rand_c: float,
    ) -> dt.Struct(
        {
            "email_from": str,
            "email_to": str,
            "name_to": str,
        }
    ):
        """
        Generate records of fake data.
        """
        res = {
            "email_from": faker.random_element(from_emails),
            "email_to": faker.email(),
            "name_to": faker.name(),
        }

        return res

    t = (
        t.mutate(
            faked=fake_row(
                t["timestamp"],
                t["rand_a"],
                t["rand_b"],
                t["rand_c"],
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
