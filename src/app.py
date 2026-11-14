"""Dash app: layout and callbacks."""
from __future__ import annotations
from dash import Dash, html, Input, Output, callback
from paths import resource_path
from data import df, apply_filter
from components import kpi_card, filter_panel

TITLE = "Student Dropout Risk"


def build_layout() -> html.Div:
    return html.Div([
        html.H1(TITLE),
        filter_panel(),
        html.Div([
            kpi_card("kpi-students", "Students"),
            kpi_card("kpi-dropout", "Dropout rate"),
            kpi_card("kpi-overall", "vs. Overall"),
            kpi_card("kpi-work", "Working part-time"),
            kpi_card("kpi-sleep", "Avg. sleep"),
            kpi_card("kpi-stress", "Avg. stress (1-10)")
        ], className="kpi-row")
    ], className="page")


def register_callbacks(app: Dash) -> None:
    @app.callback(
        Output("kpi-students", "children"),
        Output("kpi-dropout", "children"),
        Output("kpi-overall", "children"),
        Output("kpi-work", "children"),
        Output("kpi-sleep", "children"),
        Output("kpi-stress", "children"),
        Input("f-age", "value"),
        Input("f-gender", "value"),
        Input("f-first-gen", "value"),
        Input("f-income", "value"),
        Input("f-course-type", "value"),
        Input("f-study-mode", "value"),
        Input("f-semester", "value")
    )
    def update(age_range, gender, first_generation, family_income_level, course_type, study_mode, semester):
        d = apply_filter(age_range, gender, first_generation, family_income_level, course_type, study_mode, semester)
        overall_dropout = df['dropout'].mean()
        filtered_dropout = d['dropout'].mean()
        diff = (filtered_dropout - overall_dropout) * 100
        return (
            f"{len(d):,}",                                              
            f"{filtered_dropout:.1%}",                                           
            f"{overall_dropout:.1%}",       
            f"{d["part_time_job"].mean():.1%}",    
            f"{d["sleep_hours"].mean():.1f} h",                         
            f"{d["stress_level"].mean():.1f}",
            )


def create_app() -> Dash:
    app = Dash(__name__, title=TITLE, assets_folder=str(resource_path("assets")))
    app.layout = build_layout()
    register_callbacks(app)
    return app
