from ascend.resources import ref, task


@task(
    dependencies=[
        ref("staff"),
        ref("oranges"),
    ]
)
def send_staff_reports(
    staff,
    oranges,
    context,
):
    for contact in staff["contact"].to_pyarrow().to_pylist():
        print(f"Sending report to {contact}")
        print(f"{contact}: good job!")
