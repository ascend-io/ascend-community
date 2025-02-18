# imports
import os
import ibis

from rich import print
from random import random
from datetime import UTC, datetime, timedelta

from ottos_oranges.lib.seed import (
    orange_farms_csv,
    orange_warehouses_csv,
    orange_stores_csv,
    orange_types_csv,
)

# constants
LAKE_DIR = "lake"
SEED_DIR = os.path.join(LAKE_DIR, "seed")
GENERATED_DIR = os.path.join(LAKE_DIR, "generated")
EVENTS_DIR = os.path.join(GENERATED_DIR, "events")
UPLOAD_DIR = os.path.join(GENERATED_DIR, "upload")

SECONDS_PER_SECOND = 1
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR


# functions
## base tables
def tn(
    n: int = 10,
) -> ibis.Table:
    t = ibis.range(0, n).unnest().name("index").as_table()
    t = t.order_by("index")

    return t


def ts(
    start_time: str | datetime = None,
    end_time: str | datetime = None,
    interval_seconds: int = 1,
) -> ibis.Table:
    if start_time is None:
        start_time = datetime.now(UTC)
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if end_time is None:
        end_time = start_time + timedelta(days=1)

    step = ibis.interval(seconds=interval_seconds)
    t = (
        ibis.range(
            ibis.timestamp(start_time),
            ibis.timestamp(end_time),
            step=step,
        )
        .unnest()
        .name("timestamp")
        .as_table()
    )
    t = t.order_by("timestamp")

    return t


## add columns
def add_uuid_col(
    t: ibis.Table, col: str = "id", cast_to_str: bool = True
) -> ibis.Table:
    return t.mutate(**{col: ibis.uuid().cast(str) if cast_to_str else ibis.uuid()})


def add_random_col(t: ibis.Table, col: str = "rand") -> ibis.Table:
    return t.mutate(**{col: ibis.random()})


## modify number of rows
def downsample(t: ibis.Table, downsample_factor: float) -> ibis.Table:
    assert 0 < downsample_factor < 1, "downsample factor must be between 0 and 1"
    # goofier
    original_schema = t.schema()

    # downsample logic
    t = t.mutate(_downsample_on=ibis.random())
    t = t.filter(t["_downsample_on"] < downsample_factor)
    t = t.drop("_downsample_on")

    # goofier
    t = t.mutate(
        **{col: ibis._[col].cast(_type) for col, _type in dict(original_schema).items()}
    )

    # goofy
    return t.cache()


def duplicate(t: ibis.Table, duplicate_factor: float) -> ibis.Table:
    assert 0 < duplicate_factor < 1, "duplicate factor must be between 0 and 1"
    # goofier
    original_schema = t.schema()

    # duplicate logic
    t2 = downsample(t, duplicate_factor)

    # goofier
    t2 = t2.mutate(
        **{col: ibis._[col].cast(_type) for col, _type in dict(original_schema).items()}
    )

    # add the downsampled table to the original table
    t = t.union(t2)

    # goofy
    return t.cache()


## modify randomness
def walk(t: ibis.Table, walk_cols: list[str]) -> ibis.Table:
    window = ibis.window(order_by="timestamp", preceding=None, following=0)
    walked = t.mutate(**{col: t[col].sum().over(window) for col in walk_cols})
    walked = walked.relocate(t.columns).order_by("timestamp")
    return walked


## define simulation run
def run_simulation(days: int = 365):
    # ensure lake directories exist
    os.makedirs(SEED_DIR, exist_ok=True)
    os.makedirs(EVENTS_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # ensure the seed data exists
    filename = os.path.join(SEED_DIR, "orange_farms.csv")
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(orange_farms_csv)

    filename = os.path.join(SEED_DIR, "orange_warehouses.csv")
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(orange_warehouses_csv)

    filename = os.path.join(SEED_DIR, "orange_stores.csv")
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(orange_stores_csv)

    filename = os.path.join(SEED_DIR, "orange_types.csv")
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(orange_types_csv)

    # variables
    now = datetime.now(UTC).date()

    # seed tables
    orange_farms = (
        ibis.read_csv(os.path.join(SEED_DIR, "orange_farms.csv"), sep=";")
        .rename("snake_case")
        .cache()
    )
    orange_types = (
        ibis.read_csv(os.path.join(SEED_DIR, "orange_types.csv"), sep=",")
        .rename("snake_case")
        .cache()
    )
    orange_stores = (
        ibis.read_csv(os.path.join(SEED_DIR, "orange_stores.csv"), sep="|")
        .rename("snake_case")
        .cache()
    )
    orange_warehouses = (
        ibis.read_csv(os.path.join(SEED_DIR, "orange_warehouses.csv"), sep=";")
        .rename("snake_case")
        .cache()
    )

    # get random choices
    farm_ids = orange_farms.rename("snake_case")["farm_id"].to_pyarrow().to_pylist()
    orange_skus = (
        orange_types.rename("snake_case")["orange_sku"].to_pyarrow().to_pylist()
    )
    store_ids = orange_stores.rename("snake_case")["store_id"].to_pyarrow().to_pylist()
    warehouse_ids = (
        orange_warehouses.rename("snake_case")["warehouse_id"].to_pyarrow().to_pylist()
    )

    locations = sorted(
        list(
            set(
                (
                    orange_farms["farm_location"].to_pyarrow().to_pylist()
                    + orange_stores["store_location"].to_pyarrow().to_pylist()
                    + orange_warehouses["warehouse_location"].to_pyarrow().to_pylist()
                )
            )
        )
    )

    feedbacks = ["negative", "neutral", "positive"]
    feedback_comments = [
        "wow",
        "awful",
        "brilliant",
        "orange you glad I didn't say banana",
        "meh",
    ]

    # setup reusable case statements
    n_farms = len(farm_ids)
    farm_id_tuples = [
        (
            ibis._["farm_id"].between((i / n_farms), ((i + 1) / n_farms)),
            ibis.literal(farm_id),
        )
        for i, farm_id in enumerate(farm_ids)
    ]
    farm_id_cases = ibis.cases(*farm_id_tuples, else_=None)

    n_skus = len(orange_skus)
    orange_sku_tuples = [
        (
            ibis._["orange_sku"].between((i / n_skus), ((i + 1) / n_skus)),
            ibis.literal(orange_sku),
        )
        for i, orange_sku in enumerate(orange_skus)
    ]
    orange_sku_cases = ibis.cases(*orange_sku_tuples, else_=None)

    n_stores = len(store_ids)
    store_id_tuples = [
        (
            ibis._["store_id"].between((i / n_stores), ((i + 1) / n_stores)),
            ibis.literal(store_id),
        )
        for i, store_id in enumerate(store_ids)
    ]
    store_id_cases = ibis.cases(*store_id_tuples, else_=None)

    n_warehouses = len(warehouse_ids)
    warehouse_id_tuples = [
        (
            ibis._["warehouse_id"].between(
                (i / n_warehouses), ((i + 1) / n_warehouses)
            ),
            ibis.literal(warehouse_id),
        )
        for i, warehouse_id in enumerate(warehouse_ids)
    ]
    warehouse_id_cases = ibis.cases(*warehouse_id_tuples, else_=None)

    n_locations = len(locations)
    location_tuples = [
        (
            ibis._["location"].between((i / n_locations), ((i + 1) / n_locations)),
            ibis.literal(location),
        )
        for i, location in enumerate(locations)
    ]
    location_cases = ibis.cases(*location_tuples, else_=None)

    n_feedbacks = len(feedbacks)
    feedback_tuples = [
        (
            ibis._["feedback"].between((i / n_feedbacks), ((i + 1) / n_feedbacks)),
            ibis.literal(feedback),
        )
        for i, feedback in enumerate(feedbacks)
    ]
    feedback_cases = ibis.cases(*feedback_tuples, else_=None)

    n_feedback_comments = len(feedback_comments)
    feedback_comment_tuples = [
        (
            ibis._["feedback_comment"].between(
                (i / n_feedback_comments), ((i + 1) / n_feedback_comments)
            ),
            ibis.literal(feedback_comment),
        )
        for i, feedback_comment in enumerate(feedback_comments)
    ]
    feedback_comment_cases = ibis.cases(*feedback_comment_tuples, else_=None)

    # for each day in the simulation...
    for day in range(days):
        day = days - day
        day = now - timedelta(days=day)
        print(day)

        # common variables
        prev_day = day - timedelta(days=1)
        partition_path = os.path.join(
            f"year={day.year}", f"month={day.month}", f"day={day.day}"
        )
        prev_partition_path = os.path.join(
            f"year={prev_day.year}", f"month={prev_day.month}", f"day={prev_day.day}"
        )

        # simulate the orange_telemetry table
        ## variables
        tablename = "orange_telemetry.parquet"
        filename = "data.parquet"
        finalcols = [
            "timestamp",
            "orange_id",
            "orange_sku",
            "location",
            "status",
            "origin_farm_id",
        ]
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)

        ## create today's data
        o_telemetry_t = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE * 8)
            .cross_join(orange_types.rename("snake_case").select("orange_sku"))
            .mutate(orange_id=ibis.uuid().cast(str))
            .mutate(location=ibis.random())
            .mutate(location=location_cases)
            .mutate(status=ibis.literal("active"))
            .mutate(farm_id=ibis.random())
            .mutate(origin_farm_id=farm_id_cases.cast("int32"))
            .select(*finalcols)
        )
        ## check for previous day's data
        if os.path.exists(prev_filepath):
            ## read previous day's data
            o_telemetry_t_prev = ibis.read_parquet(prev_filepath)

            ## filter out inactive statuses
            o_telemetry_t_prev = o_telemetry_t_prev.filter(ibis._["status"] == "active")

            ## adjust the timestamps
            o_telemetry_t_prev = o_telemetry_t_prev.mutate(
                timestamp=(
                    o_telemetry_t_prev["timestamp"] + ibis.interval(days=1)
                ).cast("timestamp")
            )

            ## randomly update status
            o_telemetry_t_prev = o_telemetry_t_prev.mutate(new_status=ibis.random())

            unknown_frac = random() / 5
            sold_frac = unknown_frac + (random() / 2)
            sold_in_transit_frac = sold_frac + (random() / 3)

            o_telemetry_t_prev = o_telemetry_t_prev.mutate(
                status=ibis.cases(
                    (ibis._["new_status"] < unknown_frac, ibis.literal("unknown")),
                    (ibis._["new_status"] < sold_frac, ibis.literal("sold")),
                    (
                        ibis._["new_status"] < sold_in_transit_frac,
                        ibis.literal("sold (in transit)"),
                    ),
                    else_=ibis.literal("active"),
                )
            ).drop("new_status")

            o_telemetry_t_prev = o_telemetry_t_prev.select(*finalcols)

            ## update today's data with previous day's data
            o_telemetry_t = o_telemetry_t_prev.union(o_telemetry_t)

        # explicitly cast all columns
        o_telemetry_t = o_telemetry_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            orange_id=ibis._["orange_id"].cast("string"),
            orange_sku=ibis._["orange_sku"].cast("string"),
            location=ibis._["location"].cast("string"),
            status=ibis._["status"].cast("string"),
            origin_farm_id=ibis._["origin_farm_id"].cast("int32"),
        )

        ## randomly drop some data
        o_telemetry_t = downsample(o_telemetry_t, 0.9)

        ## randomly duplicate some data
        o_telemetry_t = duplicate(o_telemetry_t, 0.02)

        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            o_telemetry_t.to_parquet(filepath)

        # simulate the store_sales and website_sales tables
        ## create today's data
        sales_t = (
            o_telemetry_t.filter(
                (ibis._["status"] == "sold") | (ibis._["status"] == "sold (in transit)")
            )
            .group_by("orange_id")
            .agg(timestamp=ibis._["timestamp"].max())
        ).select("timestamp", "orange_id")

        sales_t = sales_t.mutate(store_id=ibis.random())
        sales_t = sales_t.mutate(store_id=store_id_cases)
        sales_t = sales_t.mutate(id=ibis.uuid().cast(str))
        sales_t = sales_t.mutate(price=ibis.random() * 10)
        sales_t = sales_t.select("timestamp", "id", "store_id", "orange_id", "price")

        # explicitly cast all columns
        sales_t = sales_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast("string"),
            store_id=ibis._["store_id"].cast("int32"),
            orange_id=ibis._["orange_id"].cast("string"),
            price=ibis._["price"].cast("double"),
        )

        sales_t = duplicate(sales_t, 0.03)

        ## website sales
        tablename = "website_sales.parquet"
        filename = "data.parquet"

        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            ## TODO: hardcoding here
            sales_t.filter(ibis._["store_id"] == 0).to_parquet(filepath)

        ## store sales
        tablename = "store_sales.parquet"
        filename = "data.parquet"

        for store_id in store_ids:
            if store_id == 0:
                continue
            filepath = os.path.join(
                EVENTS_DIR, tablename, f"store_id={store_id}", partition_path, filename
            )
            if os.path.exists(filepath):
                print(f"\tskipping {filepath}...")
            else:
                print(f"\twriting {filepath}...")
                os.makedirs(
                    os.path.join(
                        EVENTS_DIR, tablename, f"store_id={store_id}", partition_path
                    ),
                    exist_ok=True,
                )
                sales_t.filter(ibis._["store_id"] == store_id).to_parquet(filepath)

        ## simulate feedback table
        feedback_t = (sales_t.select("timestamp", "store_id", "orange_id")).pipe(
            downsample, 0.05
        )

        feedback_t = feedback_t.mutate(feedback=ibis.random())
        feedback_t = feedback_t.mutate(feedback=feedback_cases)
        feedback_t = feedback_t.mutate(feedback_comment=ibis.random())
        feedback_t = feedback_t.mutate(feedback_comment=feedback_comment_cases)
        feedback_t = feedback_t.mutate(id=ibis.uuid().cast(str))
        feedback_t = feedback_t.select(
            "timestamp", "id", "store_id", "orange_id", "feedback", "feedback_comment"
        )

        # explicitly cast all columns
        feedback_t = feedback_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast("string"),
            store_id=ibis._["store_id"].cast("int32"),
            orange_id=ibis._["orange_id"].cast("string"),
            feedback=ibis._["feedback"].cast("string"),
            feedback_comment=ibis._["feedback_comment"].cast("string"),
        )

        feedback_t = duplicate(feedback_t, 0.23)

        ## website feedback
        tablename = "website_feedback.parquet"
        filename = "data.parquet"

        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            feedback_t.filter(ibis._["store_id"] == 0).to_parquet(filepath)

        ## store feedback
        tablename = "store_feedback.csv"
        filename = "data.csv"

        for store_id in store_ids:
            if store_id == 0:
                continue
            filepath = os.path.join(
                UPLOAD_DIR, tablename, f"store_id={store_id}", partition_path, filename
            )
            if os.path.exists(filepath):
                print(f"\tskipping {filepath}...")
            else:
                print(f"\twriting {filepath}...")
                os.makedirs(
                    os.path.join(
                        UPLOAD_DIR, tablename, f"store_id={store_id}", partition_path
                    ),
                    exist_ok=True,
                )
                feedback_t.filter(ibis._["store_id"] == store_id).to_csv(filepath)

        ## simulate twitter data
        tablename = "twitter.parquet"
        filename = "data.parquet"

        twitter_t = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(tweet_content=ibis.literal("I love oranges!"))
            .select("timestamp", "id", "user_id", "tweet_content")
        )

        # explicitly cast all columns
        twitter_t = twitter_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast("string"),
            user_id=ibis._["user_id"].cast("string"),
            tweet_content=ibis._["tweet_content"].cast("string"),
        )

        twitter_t = downsample(twitter_t, 0.8)
        twitter_t = downsample(twitter_t, 0.9)
        twitter_t = duplicate(twitter_t, 0.13)

        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            twitter_t.to_parquet(filepath)

        ## simulate metabook data
        tablename = "metabook.parquet"
        filename = "data.parquet"

        metabook_t = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(metabook_content=ibis.literal("wow"))
            .select("timestamp", "id", "user_id", "metabook_content")
        )

        # explicitly cast all columns
        metabook_t = metabook_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast("string"),
            user_id=ibis._["user_id"].cast("string"),
            metabook_content=ibis._["metabook_content"].cast("string"),
        )

        metabook_t = downsample(metabook_t, 0.8)
        metabook_t = downsample(metabook_t, 0.9)
        metabook_t = duplicate(metabook_t, 0.13)

        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            metabook_t.to_parquet(filepath)

        ## simulate metagram data
        tablename = "metagram.parquet"
        filename = "data.parquet"

        metagram_t = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(metagram_content=ibis.literal("cool"))
            .select("timestamp", "id", "user_id", "metagram_content")
        )

        # explicitly cast all columns
        metagram_t = metagram_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast("string"),
            user_id=ibis._["user_id"].cast("string"),
            metagram_content=ibis._["metagram_content"].cast("string"),
        )

        metagram_t = downsample(metagram_t, 0.8)
        metagram_t = duplicate(metagram_t, 0.13)

        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            metagram_t.to_parquet(filepath)

        ## simulate inlinked data
        tablename = "inlinked.parquet"
        filename = "data.parquet"

        inlinked_t = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(inlinked_content=ibis.literal("interesting"))
            .select("timestamp", "id", "user_id", "inlinked_content")
        )

        # explicitly cast all columns
        inlinked_t = inlinked_t.mutate(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast("string"),
            user_id=ibis._["user_id"].cast("string"),
            inlinked_content=ibis._["inlinked_content"].cast("string"),
        )

        inlinked_t = downsample(inlinked_t, 0.5)
        inlinked_t = downsample(inlinked_t, 0.6)

        filepath = os.path.join(EVENTS_DIR, tablename, partition_path, filename)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            inlinked_t.to_parquet(filepath)
