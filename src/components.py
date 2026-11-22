from dash import html, dcc
from data import df

AGE_MIN, AGE_MAX = int(df["age"].min()), int(df["age"].max())


def age_marks(selected):
    """Only the selected ages get a visible label"""
    lo, hi = selected
    return {
        age: (str(age) if age in (lo, hi) else "")
        for age in range(AGE_MIN, AGE_MAX + 1)
    }


def kpi_card(card_id, label):
    return html.Div(
        [
            html.Div(label, className="kpi-label"),
            html.Div(id=card_id, className="kpi-value"),
        ],
        className="kpi-card",
    )


def filter_panel():
    return html.Div(
        [
            html.Div(
                [
                    html.Label("Age"),
                    dcc.RangeSlider(
                        AGE_MIN,
                        AGE_MAX,
                        1,
                        value=[AGE_MIN, AGE_MAX],
                        marks=age_marks([AGE_MIN, AGE_MAX]),
                        allow_direct_input=False,  # hide the number boxes on both sides
                        id="f-age",
                    ),
                ],
                className="filter-age",
            ),
            html.Div(
                [
                    html.Label("Gender"),
                    dcc.Dropdown(
                        sorted(df["gender"].dropna().unique()),
                        id="f-gender",
                        placeholder="All",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("First generation"),
                    dcc.Dropdown(
                        options=[
                            {"label": "Yes", "value": 1},
                            {"label": "No", "value": 0},
                        ],
                        id="f-first-gen",
                        placeholder="All",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Family income"),
                    dcc.Dropdown(
                        sorted(df["family_income_level"].dropna().unique()),
                        id="f-income",
                        placeholder="All",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Course type"),
                    dcc.Dropdown(
                        sorted(df["course_type"].dropna().unique()),
                        id="f-course-type",
                        placeholder="All",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Study mode"),
                    dcc.Dropdown(
                        sorted(df["study_mode"].dropna().unique()),
                        id="f-study-mode",
                        placeholder="All",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Semester"),
                    dcc.Dropdown(
                        sorted(df["semester"].dropna().unique()),
                        id="f-semester",
                        placeholder="All",
                    ),
                ]
            ),
        ],
        className="filter-bar",
    )
