from ascend.resources import task, ref

@task(dependencies=[ref("int_orange_farms")])
def testtask(int_orange_farms, context):
  # add your Task logic here, you can reference name for this component by using context.component_name
  context.ibis.create_table(context.component_name, int_orange_farms, overwrite=True)
