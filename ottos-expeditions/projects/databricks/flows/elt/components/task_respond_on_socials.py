import ibis

from ascend.resources import ref, task
from ascend.application.context import ComponentExecutionContext


@task(
    dependencies=[
        ref("social_media"),
    ]
)
def task_respond_on_socials(
    social_media: ibis.Table, context: ComponentExecutionContext
) -> None:
    for i in range(1000):
        print("Thank you for your comment!")
