import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_sales_vendors")])
def sales_vendors(read_sales_vendors: ibis.Table, context) -> ibis.Table:
    sales_vendors = T.clean(read_sales_vendors)
    return sales_vendors
