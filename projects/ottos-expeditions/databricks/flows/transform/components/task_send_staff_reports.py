import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("staff"),
        ref("ascenders"),
        ref("sales"),
    ]
)
def task_send_staff_reports(
    staff: ibis.Table,
    ascenders: ibis.Table,
    sales: ibis.Table,
    context: ComponentExecutionContext,
):
    for contact in staff["contact"].to_pyarrow().to_pylist():
        log(f"{contact}: good job!")
