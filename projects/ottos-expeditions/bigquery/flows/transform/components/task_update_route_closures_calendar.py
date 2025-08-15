import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("route_closures"),
    ]
)
def task_update_route_closures_calendar(
    route_closures: ibis.Table,
    context: ComponentExecutionContext,
) -> None:
    for route in route_closures["route_id"].to_pyarrow().to_pylist():
        log(f"Updaitng route {route}")
