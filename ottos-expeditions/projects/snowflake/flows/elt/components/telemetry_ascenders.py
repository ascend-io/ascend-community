import snowflake

import local_code.transform as T

from ascend.resources import ref, snowpark
from ascend.application.context import ComponentExecutionContext


@snowpark(inputs=[ref("read_telemetry_ascenders")])
def telemetry_ascenders(
    read_telemetry_ascenders: snowflake.snowpark.Table,
    context: ComponentExecutionContext,
) -> snowflake.snowpark.Table:
    telemetry_ascenders = T.clean(read_telemetry_ascenders)
    return telemetry_ascenders
