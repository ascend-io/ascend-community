from ibis import ir

from ascend.resources import ref, transform


@transform(inputs=[ref("azure_reader")])
def my_python_transform(azure_reader: ir.Table, context) -> ir.Table:
    # lake_reader is an Ibis Table object containing records from the lake_reader component
    return azure_reader
