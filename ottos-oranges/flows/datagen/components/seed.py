import ibis

from ascend.resources import read


@read()
def seed(ctx):
    lookback = ibis.interval(days=7)
    step = ibis.interval(hours=1)

    t = (
        (
            ibis.range(
                ibis.now() - lookback,
                ibis.now(),
                step=step,
            )
            .unnest()
            .name("timestamp")
            .as_table()
        )
        .mutate(
            index=(ibis.row_number().over(order_by="timestamp")),
            **{col: 2 * (ibis.random() - 0.5) for col in ["a", "b", "c"]},
        )
        .mutate(color=ibis._["index"].histogram(nbins=8))
        .drop("index")
        .relocate("timestamp", "color")
        .order_by("timestamp")
    )

    yield "partition", t
