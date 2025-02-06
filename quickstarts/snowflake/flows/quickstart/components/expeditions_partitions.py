from ibis import ir

from ascend.resources import ref, test, transform

@transform(
    inputs=[
        ref("raw_expeditions", reshape={"time": {"column": "expedition_start_date", "granularity": "day"}}),
    ],
    tests=[]
)
def expeditions_partitioned(raw_expeditions: ir.Table, context) -> ir.Table:
    return raw_expeditions
