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
def datagen(days: int = typer.Option(365, help="days", show_default=True)):
    """
    datagen
    """
    from ottos_oranges.lib.synthetic import run_simulation

    run_simulation(days=days)


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
    from ottos_oranges.ui.gui import app  # noqa

    if prod:
        run_gui_app(
            app=app,
            host="0.0.0.0",
            port=port,
        )
    else:
        run_gui_app(
            app="ottos_oranges.ui.gui:app",  # goofy! but needed to reload
            host="0.0.0.0",
            port=port,
            reload=True,
            launch_browser=True,
        )


# if __name__ == "__main__":
if __name__ == "__main__":
    app()
