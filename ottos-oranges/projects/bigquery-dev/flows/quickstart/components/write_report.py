import os
from ascend.resources import task, ref


@task(dependencies=[ref("grouped_store")])
def write_report(grouped_store, context):
    report = f"a,b,c"
    print(report)