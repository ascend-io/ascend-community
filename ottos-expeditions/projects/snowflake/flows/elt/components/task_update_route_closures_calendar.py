import ibis

from ascend.resources import ref, task
from ascend.application.context import ComponentExecutionContext


@task(
    dependencies=[
        ref("route_closures"),
    ]
)
def task_update_route_closures_calendar(
    route_closures: ibis.Table,
    context: ComponentExecutionContext,
) -> None:
    for route in route_closures["ROUTE_ID"].to_pyarrow().to_pylist():
        print(f"Updaitng route {route}")
