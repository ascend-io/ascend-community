from ascend.resources import ref, transform

@transform(inputs=[ref("staff")])
def this is a component(staff):
  # add your Transform logic here
  return staff
