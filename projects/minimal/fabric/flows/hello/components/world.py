from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import task


@task()
def world(context: ComponentExecutionContext) -> None:
    """A simple hello world task component."""
    log("Hello, world!")
