from ascend.resources import ref, task


@task(
    dependencies=[ref("expand")],
)
def writer(expand, context) -> None:
    expand.to_delta("data/data.delta", mode="overwrite")
