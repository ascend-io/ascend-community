# imports
import ibis

import ibis.expr.datatypes as dt

from faker import Faker
from collections import OrderedDict

from ottos_oranges.lib.synthetic.common import SyntheticTable

# configuration
num_stores = 100
store_names = OrderedDict({f"store_{i}": 1 / num_stores for i in range(num_stores)})


# class
class StoreEvents(SyntheticTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def transform(t: ibis.Table) -> ibis.Table:
        faker = Faker()

        @ibis.udf.scalar.python
        def fake_row(
            timestamp: dt.timestamp,
            rand_a: float,
            rand_b: float,
            rand_c: float,
        ) -> dt.Struct(
            {
                "store_name": str,
            }
        ):
            """
            Generate records of fake data.
            """
            res = {
                "store_name": faker.random_element(store_names),
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
