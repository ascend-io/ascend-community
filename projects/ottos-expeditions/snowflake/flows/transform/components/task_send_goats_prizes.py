import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("goats"),
    ]
)
def task_send_goats_prizes(
    goats: ibis.Table,
    context: ComponentExecutionContext,
) -> None:
    for goat in goats.limit(1000)["ID"].to_pyarrow().to_pylist():
        log(f"Sending prize to goat {goat}")
