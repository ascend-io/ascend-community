from ascend.resources import ref, task


@task(
    dependencies=[
        ref("expeditions"),
        ref("expeditions_partitioned"),
    ]
)
def my_task(expeditions, context):
    pass