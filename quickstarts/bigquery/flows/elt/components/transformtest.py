from ascend.resources import ref, transform

@transform(inputs=[ref("int_orange_farms")])
def transformtest(int_orange_farms):
  # add your Transform logic here
  return int_orange_farms
