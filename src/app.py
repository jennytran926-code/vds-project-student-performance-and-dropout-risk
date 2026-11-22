"""Dash app: layout and callbacks."""

from __future__ import annotations
from dash import Dash, dcc, html, Input, Output
from paths import resource_path
from data import df, apply_filter
from components import kpi_card, filter_panel, age_marks, AGE_MIN, AGE_MAX
from charts import income_job_bars, hours_income_heatmap

TITLE = "Student Dropout Risk"


def build_layout() -> html.Div:
    return html.Div(
        [
            html.H1(TITLE),
            filter_panel(),
            html.Div(
                [
                    kpi_card("kpi-students", "Students"),
                    kpi_card("kpi-dropout", "Dropout rate"),
                    kpi_card("kpi-overall", "Overall Dropout Rate"),
                    kpi_card("kpi-work", "Working part-time"),
                    kpi_card("kpi-sleep", "Avg. sleep"),
                    kpi_card("kpi-stress", "Avg. stress (1-10)"),
                ],
                className="kpi-row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H3(
                                "Dropout rate by family income, split by part-time job"
                            ),
                            dcc.Graph(
                                id="chart-a",
                                className="chart-graph",
                                style={"height": "100%"},
                                config={"displayModeBar": False, "responsive": True},
                            ),
                        ],
                        className="chart-card",
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Dropout rate by weekly work hours and family income"
                            ),
                            dcc.Graph(
                                id="chart-b",
                                className="chart-graph",
                                style={"height": "100%"},
                                config={"displayModeBar": False, "responsive": True},
                            ),
                        ],
                        className="chart-card",
                    ),
                    # TODO chart
                    html.Div(
                        "",
                        className="chart-card",
                    ),
                    # TODO chart
                    html.Div(
                        "",
                        className="chart-card",
                    ),
                ],
                className="chart-row",
            ),
        ],
        className="page",
    )


def register_callbacks(app: Dash) -> None:
    @app.callback(Output("f-age", "marks"), Input("f-age", "drag_value"))
    def update_age_marks(drag_value):
        # drag_value updates while dragging, so the labels follow the handles live
        return age_marks(drag_value or [AGE_MIN, AGE_MAX])

    @app.callback(
        Output("kpi-students", "children"),
        Output("kpi-dropout", "children"),
        Output("kpi-overall", "children"),
        Output("kpi-work", "children"),
        Output("kpi-sleep", "children"),
        Output("kpi-stress", "children"),
        Output("chart-a", "figure"),
        Output("chart-b", "figure"),
        Input("f-age", "value"),
        Input("f-gender", "value"),
        Input("f-first-gen", "value"),
        Input("f-income", "value"),
        Input("f-course-type", "value"),
        Input("f-study-mode", "value"),
        Input("f-semester", "value"),
    )
    def update(
        age_range,
        gender,
        first_generation,
        family_income_level,
        course_type,
        study_mode,
        semester,
    ):
        d = apply_filter(
            age_range,
            gender,
            first_generation,
            family_income_level,
            course_type,
            study_mode,
            semester,
        )

        def kpi_mean(col, fmt):
            return "-" if d.empty else fmt.format(d[col].mean())

        overall_dropout = df["dropout"].mean()
        return (
            f"{len(d):,}",
            kpi_mean("dropout", "{:.1%}"),
            f"{overall_dropout:.1%}",
            kpi_mean("part_time_job", "{:.1%}"),
            kpi_mean("sleep_hours", "{:.1f} h"),
            kpi_mean("stress_level", "{:.1f}"),
            income_job_bars(d),
            hours_income_heatmap(d),
        )


def create_app() -> Dash:
    app = Dash(__name__, title=TITLE, assets_folder=str(resource_path("assets")))
    app.layout = build_layout()
    register_callbacks(app)
    return app
