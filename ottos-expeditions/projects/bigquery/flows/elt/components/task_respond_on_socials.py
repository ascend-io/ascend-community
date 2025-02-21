from ascend.resources import ref, task


@task(
    dependencies=[
        ref("social_media"),
    ]
)
def task_send_goats_prizes(
    social_media,
    context,
):
    for i in range(1000):
        print("Thank you for your comment!")
