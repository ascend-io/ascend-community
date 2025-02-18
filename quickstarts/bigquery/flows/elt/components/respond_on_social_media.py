from ascend.resources import ref, task


@task(
    dependencies=[
        ref("social_media"),
        ref("oranges"),
    ]
)
def respond_on_social_media(
    social_media,
    oranges,
    context,
):
    for i in range(1000):
        print(
            "I will not use AI to automatically respond to every complaint about my product on social media..."
        )
