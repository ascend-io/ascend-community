import ibis

from ascend.resources import ref, task
from ascend.common.events import log
from ascend.application.context import ComponentExecutionContext


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
    for contact in staff["CONTACT"].to_pyarrow().to_pylist():
        log(f"{contact}: good job! Sean rocks!!!")
