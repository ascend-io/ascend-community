from ascend.resources import ref, task


@task(
    dependencies=[
        ref("expeditions"),
    ]
)
def my_task(expeditions, context):
    pass