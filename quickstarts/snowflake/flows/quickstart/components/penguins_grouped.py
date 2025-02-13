from ascend.resources import ref, transform

@transform(inputs=[ref("penguins")])
def penguins_grouped(penguins, context):
  # add your Transform logic here
  return penguins