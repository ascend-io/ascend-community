from ascend.resources import ref, task


@task(dependencies=[ref("stg_local_test")])
def local_data_task(stg_local_test, context):
    for row in stg_local_test.to_pyarrow().to_pylist():
        print(row)
