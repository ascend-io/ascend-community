from ascend.resources import ref, task


@task(
    dependencies=[
        ref("expeditions_with_routes"),
    ]
)
def my_task(expeditions, context):
    pass