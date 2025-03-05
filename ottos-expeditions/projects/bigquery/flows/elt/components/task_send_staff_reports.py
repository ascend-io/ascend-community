import ibis

from ascend.resources import ref, task
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
    for contact in staff["contact"].to_pyarrow().to_pylist():
        print(f"{contact}: good job!")
