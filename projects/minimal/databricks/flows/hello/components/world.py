from ascend.resources import task
from ascend.common.events import log
from ascend.application.context import ComponentExecutionContext


@task()
def world(context: ComponentExecutionContext) -> None:
    """A simple hello world task component."""
    log("Hello, world!")
