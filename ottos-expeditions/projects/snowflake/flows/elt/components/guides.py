import ibis
import local_code.transform as T

from ascend.resources import ref, transform


@transform(inputs=[ref("read_guides")])
def guides(read_guides: ibis.Table, context) -> ibis.Table:
    guides = T.clean(read_guides)
    return guides