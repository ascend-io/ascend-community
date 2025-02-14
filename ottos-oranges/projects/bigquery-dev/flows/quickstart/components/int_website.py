from ascend.resources import ref, transform

@transform(inputs=[ref("stg_website")])
def int_website(stg_website):
  # add your Transform logic here
  return stg_website
