import os
from ascend.resources import task, ref


@task(dependencies=[ref("grouped_store")])
def write_report(grouped_store, context):
    for i in range(20):
        print(i)

    with open(os.path.join(os.getcwd(), "data", "output_csvs", "test2.csv"), "w") as f:
        f.write("a,b,c")
