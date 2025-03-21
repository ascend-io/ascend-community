from ascend.resources import task, ref

@task()
def a2(context):
  import ibis
  # add your Task logic here, you can reference name for this component by using context.component_name
  data = {
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
  }
  table = ibis.memtable(data)
  context.ibis.create_table(context.component_name, table, overwrite=True)
