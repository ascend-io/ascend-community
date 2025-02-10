# imports
import typer

# default typer kwargs
default_kwargs = {
    "no_args_is_help": True,
    "add_completion": False,
    "context_settings": {"help_option_names": ["-h", "--help"]},
}

# typer config
## main app
app = typer.Typer(help="ottos-oranges", **default_kwargs)


# commands
@app.command()
@app.command("d", hidden=True)
def datagen(
    lookback_days: int = typer.Option(
        365, "-l", "--lookback-days", help="lookback days"
    ),
    interval_seconds: int = typer.Option(
        60, "-i", "--interval-seconds", help="interval seconds"
    ),
):
    """
    datagen
    """
    import ibis
    import time

    from rich import print

    from ottos_oranges.datagen import seed, walk, fake

    ibis.options.interactive = True

    print("generating data...")

    print()
    print("\tseed:")
    start = time.time()
    s = seed(lookback_days=lookback_days, interval_seconds=interval_seconds)
    print(s.schema())
    print(s)
    s.to_delta("data/seed.delta", mode="overwrite")
    end = time.time()
    print(f"\telapsed: {end - start:.2f}s")

    print()
    print("\twalk:")
    start = time.time()
    w = walk(s)
    print(w.schema())
    print(w)
    w.to_delta("data/walked.delta", mode="overwrite")
    end = time.time()
    print(f"\telapsed: {end - start:.2f}s")

    print()
    print("\tfake:")
    start = time.time()
    f = fake(w).cache()
    print(f.schema())
    print(f)
    f.to_delta("data/faked.delta", mode="overwrite")
    end = time.time()
    print(f"\telapsed: {end - start:.2f}s")


@app.command()
@app.command("g", hidden=True)
def gui(
    port: int = typer.Option(1913, help="port", show_default=True),
    prod: bool = typer.Option(False, help="prod?", show_default=True),
):
    """
    gui
    """
    from shiny import run_app as run_gui_app
    from ottos_oranges.gui import app  # noqa

    if prod:
        run_gui_app(
            app=app,
            host="0.0.0.0",
            port=port,
        )
    else:
        run_gui_app(
            app="ottos_oranges.gui:app",  # goofy! but needed to reload
            host="0.0.0.0",
            port=port,
            reload=True,
            launch_browser=True,
        )


# if __name__ == "__main__":
if __name__ == "__main__":
    app()
