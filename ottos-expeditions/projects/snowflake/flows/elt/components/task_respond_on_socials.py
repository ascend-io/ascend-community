from ascend.resources import ref, task


@task(
    dependencies=[
        ref("social_media"),
    ]
)
def task_respond_on_socials(
    social_media,
    context,
):
    for i in range(1000):
        print("Thank you for your comment!")