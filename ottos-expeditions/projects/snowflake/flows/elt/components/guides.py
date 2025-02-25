import ibis

from ascend.resources import ref, transform


@transform(inputs=[ref("read_guides")])
def guides(read_guides: ibis.Table, context) -> ibis.Table:
    guides = read_guides.distinct()
    return guides