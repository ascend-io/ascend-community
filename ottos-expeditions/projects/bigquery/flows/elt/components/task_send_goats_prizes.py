import ibis

from ascend.resources import ref, task
from ascend.application.context import ComponentExecutionContext


@task(
    dependencies=[
        ref("goats"),
    ]
)
def task_send_goats_prizes(
    goats: ibis.Table,
    context: ComponentExecutionContext,
) -> None:
    for goat in goats["id"].to_pyarrow().to_pylist():
        print(f"Sending prize to goat {goat}")
