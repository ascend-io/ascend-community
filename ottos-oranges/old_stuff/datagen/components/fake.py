# imports
import ibis
import ibis.expr.datatypes as dt

from faker import Faker
from datetime import datetime, timedelta


from ascend.resources import transform, ref


# fake data generator
faker = Faker()


@transform(inputs=[ref("walk")])
# TODO: ctx vs context here
def fake(walk, context):
    # udfs
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

    faked_t = (
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

    return faked_t
