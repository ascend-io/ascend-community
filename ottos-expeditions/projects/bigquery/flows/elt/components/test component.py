from ascend.resources import ref, transform

@transform(inputs=[ref("ascenders")])
def test component(ascenders):
  # add your Transform logic here
  return ascenders
