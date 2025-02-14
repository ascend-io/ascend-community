import ibis

from ascend.resources import ref, transform

@transform(inputs=[ref("int_store")])
def grouped_store(int_store):
  # add your Transform logic here
  return int_store.group_by(int_store["store_name"]).agg(count=ibis._.count()).order_by(ibis.desc("count"))

