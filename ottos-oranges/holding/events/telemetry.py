# imports
import ibis

import ibis.expr.datatypes as dt

from faker import Faker
from collections import OrderedDict

from ottos_oranges.lib.synthetic.common import SyntheticTable

# configuration
orange_types = OrderedDict(
    {
        "navel": 0.5,
        "mandarin": 0.3,
        "blood": 0.1,
        "valencia": 0.1,
    }
)


# class
class TelemetryEvents(SyntheticTable):
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
