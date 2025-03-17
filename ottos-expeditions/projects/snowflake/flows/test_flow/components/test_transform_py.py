from ascend.resources import ref, transform

@transform(inputs=[ref("test_read")])
def test_transform_py(test_read, context):
  # add your Transform logic here
  return test_read
