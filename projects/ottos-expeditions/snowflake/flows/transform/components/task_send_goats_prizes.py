import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("top_ascenders"),
    ]
)
def task_send_goats_prizes(
    top_ascenders: ibis.Table,
    context: ComponentExecutionContext,
) -> None:
    for ascender in top_ascenders.limit(1000)["ID"].to_pyarrow().to_pylist():
        log(f"Sending prize to Ascender {ascender}")
