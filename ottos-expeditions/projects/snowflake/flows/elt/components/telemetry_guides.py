import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_telemetry_guides")])
def telemetry_guides(
    read_telemetry_guides: snowflake.snowpark.Table, context: ComponentExecutionContext
) -> snowflake.snowpark.Table:
    telemetry_guides = T.clean(read_telemetry_guides)
    return telemetry_guides
