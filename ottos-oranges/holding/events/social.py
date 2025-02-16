# imports
import ibis

import ibis.expr.datatypes as dt

from faker import Faker
from collections import OrderedDict

from ottos_oranges.lib.synthetic.common import SyntheticTable

# configuration
social_sources = OrderedDict(
    {
        "twitter": 0.5,
        "metabook": 0.3,
        "inlinked": 0.1,
        "metagram": 0.1,
    }
)


class SocialEvents(SyntheticTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def transform(t: ibis.Table) -> ibis.Table:
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
