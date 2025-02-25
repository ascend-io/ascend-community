from ascend.resources import ref, task


@task(
    dependencies=[
        ref("goats"),
    ]
)
def task_send_goats_prizes(
    goats,
    context,
):
    for goat in goats["ID"].to_pyarrow().to_pylist():
        print(f"Sending prize to goat {goat}")