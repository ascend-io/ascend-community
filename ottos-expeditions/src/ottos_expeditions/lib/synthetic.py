# imports
import os
import ibis

from rich import print
from faker import Faker
from random import random
from datetime import UTC, datetime, timedelta

from ottos_expeditions.lib.seed import (
    stores_csv,
    warehouses_csv,
    routes_csv,
    guides_csv,
)


# functions
## base tables
def tn(
    n: int = 10,
) -> ibis.Table:
    """
    Generate a table with n rows.
    """
    t = ibis.range(0, n).unnest().name("index").as_table()
    t = t.order_by("index")

    return t


def ts(
    start_time: str | datetime = None,
    end_time: str | datetime = None,
    interval_seconds: int = 1,
) -> ibis.Table:
    """
    Generate a time series table.
    """
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


## modify number of rows
def downsample(t: ibis.Table, downsample_factor: float) -> ibis.Table:
    """
    Downsample a table to a factor.

    Why didn't I just use the sample method? Good question!

    Some goofy casting and caching that may not be needed.
    """
    assert 0 < downsample_factor < 1, "downsample factor must be between 0 and 1"
    # goofier
    t = t.cache()
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
    """
    Duplicate a table by a factor.

    Some goofy casting. Caching is sorta needed -- otherwise, the data is not actually
    duplicated. Should double check this though.

    Should this be called upsample? Is naming things hard?
    """
    assert 0 < duplicate_factor < 1, "duplicate factor must be between 0 and 1"
    # goofier
    t = t.cache()
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
def walk(
    t: ibis.Table, walk_cols: list[str] | str, index_col: str = "timestamp"
) -> ibis.Table:
    """
    Walk numeric columns; intended to perform a random walk over a timeseries.
    """
    if isinstance(walk_cols, str):
        walk_cols = [walk_cols]
    window = ibis.window(order_by=index_col, preceding=None, following=0)
    walked = t.mutate(**{col: t[col].sum().over(window) for col in walk_cols})
    walked = walked.relocate(t.columns).order_by(index_col)
    return walked


## define simulation run
def run_simulation(days: int = 365):
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

    # variables
    now = datetime.now(UTC).date()
    fake = Faker()

    # ensure lake directories exist
    os.makedirs(SEED_DIR, exist_ok=True)
    os.makedirs(GENERATED_DIR, exist_ok=True)
    os.makedirs(EVENTS_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # write and read seed data
    def write_read_seed(filename: str, data: str, sep: str = ",") -> ibis.Table:
        filename = os.path.join(SEED_DIR, filename)
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(data)
        return ibis.read_csv(filename, sep=sep).rename("snake_case").cache()

    stores = write_read_seed("stores.csv", stores_csv, sep="|")
    warehouses = write_read_seed("warehouses.csv", warehouses_csv, sep=";")
    routes = write_read_seed("routes.csv", routes_csv, sep="|")
    guides = write_read_seed("guides.csv", guides_csv, sep=",")

    # get random choices
    store_ids = stores["id"].to_pyarrow().to_pylist()
    warehouse_ids = warehouses["id"].to_pyarrow().to_pylist()
    route_ids = routes["id"].to_pyarrow().to_pylist()
    guide_ids = guides["id"].to_pyarrow().to_pylist()

    locations = sorted(
        list(
            set(
                (
                    stores["location"].to_pyarrow().to_pylist()
                    + warehouses["location"].to_pyarrow().to_pylist()
                )
            )
        )
    )
    weather_locations = locations + list(set([fake.city() for _ in range(128)]))

    feedbacks = ["negative", "neutral", "positive"]
    feedback_comments = [
        "wow",
        "awful",
        "brilliant",
        "orange you glad I didn't say banana",
        "meh",
    ]

    def build_cases(column: str, values: list[str]) -> ibis.Expr:
        n_values = len(values)
        value_tuples = [
            (
                ibis._[column].between((i / n_values), ((i + 1) / n_values)),
                ibis.literal(value),
            )
            for i, value in enumerate(values)
        ]
        return ibis.cases(*value_tuples, else_=None)

    store_id_cases = build_cases("store_id", store_ids)
    warehouse_id_cases = build_cases("warehouse_id", warehouse_ids)
    location_cases = build_cases("location", locations)
    weather_location_cases = build_cases("location", weather_locations)
    feedback_cases = build_cases("feedback", feedbacks)
    feedback_content_cases = build_cases("feedback_content", feedback_comments)
    route_cases = build_cases("route_id", route_ids)
    guide_cases = build_cases("guide_id", guide_ids)

    # define table simulation
    def simulate_weather(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "weather.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        # TODO: actually use this data
        if os.path.exists(prev_filepath):
            _weather_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        weather = (
            ts(start_time=day, interval_seconds=SECONDS_PER_SECOND * 90)
            .mutate(location=ibis.random())
            .mutate(location=weather_location_cases)
            .mutate(temperature=ibis.random() * 100)
            .mutate(precipitation=ibis.random() * 100)
            .mutate(wind_speed=ibis.random() * 100)
        )

        # explicitly select and cast all columns
        weather = weather.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            location=ibis._["location"].cast(str),
            temperature=ibis._["temperature"].cast(float),
            precipitation=ibis._["precipitation"].cast(float),
            wind_speed=ibis._["wind_speed"].cast(float),
        )

        # randomly drop some data
        weather = downsample(weather, 0.9)

        # randomly duplicate some data
        weather = duplicate(weather, 0.04)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            weather.to_parquet(filepath)

        # return today's data
        return weather

    def simulate_weather_routes(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "weather_routes.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        # TODO: actually use this data
        if os.path.exists(prev_filepath):
            _weather_routes_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        weather_routes = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE * 8)
            .mutate(route_id=ibis.random())
            .mutate(route_id=route_cases)
            .mutate(ascender_id=ibis.uuid().cast(str))
            .mutate(temperature=ibis.random() * 100)
            .mutate(precipitation=ibis.random() * 100)
            .mutate(wind_speed=ibis.random() * 100)
        )

        # explicitly select and cast all columns
        weather_routes = weather_routes.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            route_id=ibis._["route_id"].cast(str),
            ascender_id=ibis._["ascender_id"].cast(str),
            temperature=ibis._["temperature"].cast(float),
            precipitation=ibis._["precipitation"].cast(float),
            wind_speed=ibis._["wind_speed"].cast(float),
        )

        # randomly drop some data
        weather_routes = downsample(weather_routes, 0.99)

        # randomly duplicate some data
        weather_routes = duplicate(weather_routes, 0.13)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            weather_routes.to_parquet(filepath)

        # return today's data
        return weather_routes

    def simulate_inlinked(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "inlinked.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        # TODO: actually use this data
        if os.path.exists(prev_filepath):
            _inlinked_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        inlinked = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(inlinked_content=ibis.literal("interesting"))
            .select("timestamp", "id", "user_id", "inlinked_content")
        )

        # explicitly cast all columns
        inlinked = inlinked.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            user_id=ibis._["user_id"].cast(str),
            inlinked_content=ibis._["inlinked_content"].cast(str),
        )

        # randomly drop some data
        inlinked = downsample(inlinked, 0.5)
        inlinked = downsample(inlinked, 0.6)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            inlinked.to_parquet(filepath)

        # return today's data
        return inlinked

    def simulate_metagram(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "metagram.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        # TODO: actually use this data
        if os.path.exists(prev_filepath):
            _metagram_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        metagram = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE * 4)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(metagram_content=ibis.literal("cool"))
            .select("timestamp", "id", "user_id", "metagram_content")
        )

        # explicitly cast all columns
        metagram = metagram.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            user_id=ibis._["user_id"].cast(str),
            metagram_content=ibis._["metagram_content"].cast(str),
        )

        # randomly drop some data
        metagram = downsample(metagram, 0.8)

        # randomly duplicate some data
        metagram = duplicate(metagram, 0.13)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            metagram.to_parquet(filepath)

        # return today's data
        return metagram

    def simulate_metabook(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "metabook.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _metabook_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        metabook = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE * 3)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(metabook_content=ibis.literal("wow"))
            .select("timestamp", "id", "user_id", "metabook_content")
        )

        # explicitly cast all columns
        metabook = metabook.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            user_id=ibis._["user_id"].cast(str),
            metabook_content=ibis._["metabook_content"].cast(str),
        )

        # randomly drop some data
        metabook = downsample(metabook, 0.7)

        # randomly duplicate some data
        metabook = duplicate(metabook, 0.45)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            metabook.to_parquet(filepath)

        # return today's data
        return metabook

    def simulate_twitter(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "twitter.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _twitter_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        twitter = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(tweet_content=ibis.literal("I love expeditions!"))
        )

        # explicitly cast all columns
        twitter = twitter.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            user_id=ibis._["user_id"].cast(str),
            tweet_content=ibis._["tweet_content"].cast(str),
        )

        # randomly drop some data
        twitter = downsample(twitter, 0.9)
        twitter = downsample(twitter, 0.9)
        twitter = duplicate(twitter, 0.23)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            twitter.to_parquet(filepath)

        # return today's data
        return twitter

    def simulate_feedback_website(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "feedback_website.parquet"
        filename = "data.parquet"

        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _feedback_website_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        feedback_website = (
            ts(start_time=day, interval_seconds=SECONDS_PER_HOUR * 2)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(user_id=ibis.uuid().cast(str))
            .mutate(feedback=ibis.random())
            .mutate(feedback=feedback_cases)
            .mutate(feedback_content=ibis.random())
            .mutate(feedback_content=feedback_content_cases)
        )

        # explicitly cast all columns
        feedback_website = feedback_website.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            user_id=ibis._["user_id"].cast(str),
            feedback_content=ibis._["feedback_content"].cast(str),
        )

        # randomly drop some data
        feedback_website = downsample(feedback_website, 0.99)

        # randomly duplicate some data
        feedback_website = duplicate(feedback_website, 0.04)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            feedback_website.to_parquet(filepath)

        # return today's data
        return feedback_website

    def simulate_feedback_store(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "feedback_store.csv"
        filename = "data.csv"

        feedback_store_all = None

        for store_id in store_ids:
            prev_filepath = os.path.join(
                EVENTS_DIR,
                tablename,
                f"store_id={store_id}",
                prev_day_partition_path,
                filename,
            )
            filepath = os.path.join(
                EVENTS_DIR,
                tablename,
                f"store_id={store_id}",
                day_partition_path,
                filename,
            )

            # read yesterday's data
            if os.path.exists(prev_filepath):
                _feedback_store_prev = ibis.read_csv(prev_filepath)

            # create today's data
            feedback_store = (
                ts(start_time=day, interval_seconds=SECONDS_PER_HOUR * 20)
                .mutate(id=ibis.uuid().cast(str))
                .mutate(store_id=ibis.random())
                .mutate(store_id=store_id_cases)
                .mutate(feedback=ibis.random())
                .mutate(feedback=feedback_cases)
                .mutate(feedback_content=ibis.random())
                .mutate(feedback_content=feedback_content_cases)
            )

            # explicitly cast all columns
            feedback_store = feedback_store.select(
                timestamp=ibis._["timestamp"].cast("timestamp"),
                id=ibis._["id"].cast(str),
                store_id=ibis._["store_id"].cast(str),
                feedback=ibis._["feedback"].cast(str),
                feedback_content=ibis._["feedback_content"].cast(str),
            )

            # randomly drop some data
            feedback_store = downsample(feedback_store, 0.98)

            # randomly duplicate some data
            feedback_store = duplicate(feedback_store, 0.01)

            # write today's data (if it doesn't already exist)
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
                feedback_store.to_csv(filepath, separator="|")

            feedback_store_all = (
                feedback_store
                if feedback_store_all is None
                else feedback_store_all.union(feedback_store)
            )

        # return today's data
        return feedback_store

    def simulate_feedback_ascenders(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "feedback_ascenders.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _feedback_ascenders_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        feedback_ascenders = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE * 5)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(ascender_id=ibis.uuid().cast(str))
            .mutate(feedback=ibis.random())
            .mutate(feedback=feedback_cases)
            .mutate(feedback_content=ibis.random())
            .mutate(feedback_content=feedback_content_cases)
        )

        # explicitly cast all columns
        feedback_ascenders = feedback_ascenders.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            ascender_id=ibis._["ascender_id"].cast(str),
            feedback=ibis._["feedback"].cast(str),
            feedback_content=ibis._["feedback_content"].cast(str),
        )

        # randomly drop some data
        feedback_ascenders = downsample(feedback_ascenders, 0.99)

        # randomly duplicate some data
        feedback_ascenders = duplicate(feedback_ascenders, 0.1)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            feedback_ascenders.to_parquet(filepath)

        # return today's data
        return feedback_ascenders

    def simulate_sales_website(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "sales_website.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _sales_website_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        sales_website = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(ascender_id=ibis.uuid().cast(str))
            .mutate(route_id=ibis.random())
            .mutate(route_id=route_cases)
            .mutate(price=ibis.random() * 100)
            .mutate(quantity=ibis.random() * 100)
            .mutate(tax=ibis.random() / 10)
        )

        # explicitly cast all columns
        sales_website = sales_website.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            ascender_id=ibis._["ascender_id"].cast(str),
            route_id=ibis._["route_id"].cast(str),
            price=ibis._["price"].cast(float),
            quantity=ibis._["quantity"].cast(float),
            tax=ibis._["tax"].cast(float),
        )

        # randomly drop some data
        # sales_website = downsample(sales_website, 0.8)

        # randomly duplicate some data
        # sales_website = duplicate(sales_website, 0.13)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            sales_website.to_parquet(filepath)

        # return today's data
        return sales_website

    def simulate_sales_store(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "sales_store.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _sales_store_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        sales_store = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE / 0.4)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(ascender_id=ibis.uuid().cast(str))
            .mutate(store_id=ibis.random())
            .mutate(store_id=store_id_cases)
            .mutate(route_id=ibis.random())
            .mutate(route_id=route_cases)
            .mutate(price=ibis.random() * 100)
            .mutate(quantity=ibis.random() * 100)
            .mutate(tax=ibis.random() / 10)
        )

        # explicitly cast all columns
        sales_store = sales_store.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            ascender_id=ibis._["ascender_id"].cast(str),
            store_id=ibis._["store_id"].cast(str),
            route_id=ibis._["route_id"].cast(str),
            price=ibis._["price"].cast(float),
            quantity=ibis._["quantity"].cast(float),
            tax=ibis._["tax"].cast(float),
        )

        # randomly drop some data
        # sales_store = downsample(sales_store, 0.8)

        # randomly duplicate some data
        # sales_store = duplicate(sales_store, 0.13)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            sales_store.to_parquet(filepath)

        # return today's data
        return sales_store

    def simulate_sales_vendors(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "sales_vendors.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _sales_vendors_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        sales_vendors = (
            ts(start_time=day, interval_seconds=SECONDS_PER_MINUTE)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(vendor_id=ibis.uuid().cast(str))
            .mutate(route_id=ibis.random())
            .mutate(route_id=route_cases)
            .mutate(price=ibis.random() * 100)
            .mutate(quantity=ibis.random() * 100)
            .mutate(tax=ibis.random() / 10)
        )

        # explicitly cast all columns
        sales_vendors = sales_vendors.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            vendor_id=ibis._["vendor_id"].cast(str),
            route_id=ibis._["route_id"].cast(str),
            price=ibis._["price"].cast(float),
            quantity=ibis._["quantity"].cast(float),
            tax=ibis._["tax"].cast(float),
        )

        # randomly drop some data
        sales_vendors = downsample(sales_vendors, 0.7)

        # randomly duplicate some data
        sales_vendors = duplicate(sales_vendors, 0.11)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            sales_vendors.to_parquet(filepath)

        # return today's data
        return sales_vendors

    def simulate_ascenders_telemetry(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "ascenders_telemetry.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _ascenders_telemetry_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        ascenders_telemetry = (
            ts(start_time=day, interval_seconds=SECONDS_PER_SECOND * 20)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(route_id=ibis.random())
            .mutate(route_id=route_cases)
            .mutate(ascender_id=ibis.uuid().cast(str))
            .mutate(progress=ibis.random())
        )

        # walk the progress column
        ascenders_telemetry = walk(ascenders_telemetry, "progress")

        # explicitly cast all columns
        ascenders_telemetry = ascenders_telemetry.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            route_id=ibis._["route_id"].cast(str),
            ascender_id=ibis._["ascender_id"].cast(str),
            progress=ibis._["progress"].cast(float),
        )

        # randomly drop some data
        ascenders_telemetry = downsample(ascenders_telemetry, 0.99)

        # randomly duplicate some data
        ascenders_telemetry = duplicate(ascenders_telemetry, 0.3)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            ascenders_telemetry.to_parquet(filepath)

        # return today's data
        return ascenders_telemetry

    def simulate_guides_telemetry(
        day: datetime,
        prev_day: datetime,
        day_partition_path: str,
        prev_day_partition_path: str,
    ) -> ibis.Table:
        # variables
        tablename = "guides_telemetry.parquet"
        filename = "data.parquet"
        prev_filepath = os.path.join(
            EVENTS_DIR, tablename, prev_day_partition_path, filename
        )
        filepath = os.path.join(EVENTS_DIR, tablename, day_partition_path, filename)

        # read yesterday's data
        if os.path.exists(prev_filepath):
            _guides_telemetry_prev = ibis.read_parquet(prev_filepath)

        # create today's data
        guides_telemetry = (
            ts(start_time=day, interval_seconds=SECONDS_PER_SECOND * 20)
            .mutate(id=ibis.uuid().cast(str))
            .mutate(route_id=ibis.random())
            .mutate(route_id=route_cases)
            .mutate(guide_id=ibis.random())
            .mutate(guide_id=guide_cases)
            .mutate(progress=ibis.random())
        )

        # walk the progress column
        guides_telemetry = walk(guides_telemetry, "progress")

        # explicitly cast all columns
        guides_telemetry = guides_telemetry.select(
            timestamp=ibis._["timestamp"].cast("timestamp"),
            id=ibis._["id"].cast(str),
            route_id=ibis._["route_id"].cast(str),
            guide_id=ibis._["guide_id"].cast(str),
            progress=ibis._["progress"].cast(float),
        )

        # randomly drop some data
        guides_telemetry = downsample(guides_telemetry, 0.9)

        # randomly duplicate some data
        guides_telemetry = duplicate(guides_telemetry, 0.3)

        # write today's data (if it doesn't already exist)
        if os.path.exists(filepath):
            print(f"\tskipping {filepath}...")
        else:
            print(f"\twriting {filepath}...")
            os.makedirs(
                os.path.join(EVENTS_DIR, tablename, partition_path), exist_ok=True
            )
            guides_telemetry.to_parquet(filepath)

        # return today's data
        return guides_telemetry

    # for each day in the simulation...
    for day in range(days):
        day = days - day
        day = now - timedelta(days=day)
        print(day)

        # common table inputs
        prev_day = day - timedelta(days=1)
        prev_partition_path = os.path.join(
            f"year={prev_day.year}", f"month={prev_day.month}", f"day={prev_day.day}"
        )
        partition_path = os.path.join(
            f"year={day.year}", f"month={day.month}", f"day={day.day}"
        )

        # simulate the tables
        # TODO: make some tables depend on others and build in interesting statistics
        _weather = simulate_weather(day, prev_day, partition_path, prev_partition_path)
        _weather_routes = simulate_weather_routes(
            day, prev_day, partition_path, prev_partition_path
        )
        _inlinked = simulate_inlinked(
            day, prev_day, partition_path, prev_partition_path
        )
        _metagram = simulate_metagram(
            day, prev_day, partition_path, prev_partition_path
        )
        _metabook = simulate_metabook(
            day, prev_day, partition_path, prev_partition_path
        )
        _twitter = simulate_twitter(day, prev_day, partition_path, prev_partition_path)
        _feedback_website = simulate_feedback_website(
            day, prev_day, partition_path, prev_partition_path
        )
        _feedback_store = simulate_feedback_store(
            day, prev_day, partition_path, prev_partition_path
        )
        _feedback_ascenders = simulate_feedback_ascenders(
            day, prev_day, partition_path, prev_partition_path
        )
        _sales_website = simulate_sales_website(
            day, prev_day, partition_path, prev_partition_path
        )
        _sales_store = simulate_sales_store(
            day, prev_day, partition_path, prev_partition_path
        )
        _sales_vendors = simulate_sales_vendors(
            day, prev_day, partition_path, prev_partition_path
        )
        _ascenders_telemetry = simulate_ascenders_telemetry(
            day, prev_day, partition_path, prev_partition_path
        )
        _guides_telemetry = simulate_guides_telemetry(
            day, prev_day, partition_path, prev_partition_path
        )
