from ascend.resources import ref, transform

@transform(inputs=[ref("penguins")])
def penguins_grouped(penguins, ctx):
  # add your Transform logic here
  return penguins