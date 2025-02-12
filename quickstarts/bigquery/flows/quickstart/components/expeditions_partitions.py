from ascend.resources import ref, snowpark, test


@transform(
    inputs=[
        ref("raw_expeditions", reshape={"time": {"column": "expedition_start_date", "granularity": "day"}}),
    ],
    tests=[
        test("count_equal", count=337),
        test("count_distinct_equal", column="_ascend_partition_uuid", count=31)
    ],
)
def expeditions_partitioned(raw_expeditions, context):
    return raw_expeditions
