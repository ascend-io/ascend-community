from ascend.resources import task, ref

@task(dependencies=[ref("int_telemetry")])
def telemetry_task(int_telemetry, context):
  # add your Task logic here, you can reference name for this component by using context.component_name
  context.ibis.create_table(context.component_name, int_telemetry, overwrite=True)
