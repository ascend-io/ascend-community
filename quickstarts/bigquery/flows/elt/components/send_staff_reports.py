from ascend.resources import ref, task


@task(
    dependencies=[
        ref("staff"),
        ref("oranges"),
        ref("sales"),
        ref("feedback"),
    ]
)
def send_staff_reports(
    staff,
    oranges,
    sales,
    context,
    feedback,
):
    for contact in staff["contact"].to_pyarrow().to_pylist():
        print(f"Sending report to {contact}")
        print(f"{contact}: good job!")
