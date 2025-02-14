from ascend.resources import task, ref

@task(dependencies=[ref("int_telemetry")])
def telemetry_task(int_telemetry, context):
  # add your Task logic here, you can reference name for this component by using context.component_name
  for i in range(20):
    print(i)