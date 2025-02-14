from ascend.resources import ref, transform

@transform(inputs=[ref("stg_website")])
def int_website(stg_websitem, context):
  return stg_website
