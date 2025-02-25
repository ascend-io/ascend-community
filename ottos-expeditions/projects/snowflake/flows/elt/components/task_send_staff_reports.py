from ascend.resources import ref, task


@task(
    dependencies=[
        ref("staff"),
        ref("ascenders"),
        ref("sales"),
    ]
)
def task_send_staff_reports(
    staff,
    ascenders,
    sales,
    context,
):
    for contact in staff["contact"].to_pyarrow().to_pylist():
        print(f"{contact}: good job!")
