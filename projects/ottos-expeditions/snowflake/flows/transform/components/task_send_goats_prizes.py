import ibis

from ascend.resources import ref, task
from ascend.common.events import log
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
    for goat in goats.limit(1000)["ID"].to_pyarrow().to_pylist():
        log(f"Sending prize to goat {goat}")
