import ibis
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import ref, task


@task(
    dependencies=[
        ref("social_media"),
    ]
)
def task_respond_on_socials(
    social_media: ibis.Table, context: ComponentExecutionContext
) -> None:
    for i in range(1000):
        log("Thank you for your comment!")
