# imports
from shiny import App, ui, module, reactive
from shinyswatch import theme

# state

# gui

gui = ui.page_sidebar(
    ui.sidebar("settings", "settings"),
    ui.h1("Otto's Oranges"),
    theme=theme.journal,
)


# server
@module.server
def module_server(input, output, session):
    def _get_id(session):
        # TODO: this isn't ideal (?)
        return str(session.ns)

    @reactive.Effect
    @reactive.event(input.button)
    def _():
        id = _get_id(session)
        id = id


def server(input, output, session):
    pass


# app
app = App(gui, server)
