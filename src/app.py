"""Dash app: layout and callbacks."""

from __future__ import annotations

from dash import Dash, html

from paths import resource_path

TITLE = "Student Dropout Risk"


def build_layout() -> html.Div:
    return html.Div([], className="page")


def register_callbacks(app: Dash) -> None:
    pass


def create_app() -> Dash:
    app = Dash(__name__, title=TITLE, assets_folder=str(resource_path("assets")))
    app.layout = build_layout()
    register_callbacks(app)
    return app
