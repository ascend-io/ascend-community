import ibis

from ascend.resources import transform, ref


@transform(inputs=[ref("seed")])
# TODO: ctx vs context here
def walk(seed, context):
    window = ibis.window(order_by="timestamp", preceding=None, following=0)
    walked = seed.select(
        "timestamp",
        "color",
        a=seed["a"].sum().over(window),
        b=seed["b"].sum().over(window),
        c=seed["c"].sum().over(window),
    ).order_by("timestamp")

    return walked
