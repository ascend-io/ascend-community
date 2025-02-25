import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_warehouses")])
def warehouses(read_warehouses: ibis.Table, context) -> ibis.Table:
    warehouses = T.clean(read_warehouses)
    return warehouses