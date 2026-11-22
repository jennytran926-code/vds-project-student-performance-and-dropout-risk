from __future__ import annotations

import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data import df

INCOME_ORDER = ["Low", "Middle", "High"]

# One hover style for all charts
HOVERLABEL = dict(
    bgcolor="white", bordercolor="#C9CED6", font=dict(color="#222", size=13)
)

YLORRD = px.colors.sequential.YlOrRd
JOB_SERIES = [
    (0, "No part-time job", YLORRD[3]),
    (1, "Part-time job", YLORRD[7]),
]


def empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, font=dict(size=14, color="#667"))
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


def income_job_bars(d: pd.DataFrame) -> go.Figure:
    """Visualization for dropout rate by family income, split by part-time job"""
    if d.empty:
        return empty_figure("No students match the current filters")

    stats = (
        d.groupby(["family_income_level", "part_time_job"])["dropout"]
        .agg(rate="mean", n="size")
        .reset_index()
    )

    fig = go.Figure()
    for job, label, color in JOB_SERIES:
        s = (
            stats[stats["part_time_job"] == job]
            .set_index("family_income_level")
            .reindex(INCOME_ORDER)
            .dropna(subset=["rate"])
        )
        fig.add_bar(
            name=label,
            x=s.index,
            y=s["rate"] * 100,
            marker_color=color,
            text=[
                f"{r:.0%}" for r in s["rate"]
            ],  # ":.0%" multiplies the rate (0-1) by 100, rounds to 0 decimals, adds "%"
            textposition="outside",
            customdata=s["n"],
            hovertemplate=(
                f"<b>%{{x}} income | {label}</b><br>"
                "Dropout rate: %{y:.1f}%<br>"
                "Students: %{customdata:,}<extra></extra>"  # the empty <extra></extra> hides Plotly's side box with the trace name
            ),
        )

    fig.update_layout(
        template="plotly_white",
        hoverlabel=HOVERLABEL,
        barmode="group",
        bargap=0.3,
        bargroupgap=0.05,
        margin=dict(l=50, r=20, t=20, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            title="Family income",
            categoryorder="array",
            categoryarray=INCOME_ORDER,
        ),
        yaxis=dict(
            title="Dropout rate (%)",
            rangemode="tozero",
            range=[0, max(stats["rate"].max() * 100 * 1.15, 10)],
            ticksuffix="%",
        ),
        uniformtext=dict(minsize=10, mode="hide"),
    )
    return fig


MAX_WORK_HOURS = int(df["weekly_work_hours"].max())
HOURS_BINS = [-1, 0, 10, 20, 30, math.inf]
HOURS_LABELS = ["0", "1-10", "11-20", "21-30", f"31-{MAX_WORK_HOURS}"]


def hours_income_rates(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Dropout rate (%) and student count per (work hours bin, income) cell."""
    hours = pd.cut(d["weekly_work_hours"], HOURS_BINS, labels=HOURS_LABELS)
    stats = d.groupby([hours, d["family_income_level"]], observed=False)["dropout"].agg(
        rate="mean", n="size"
    )
    rate = (
        stats["rate"].unstack().reindex(index=HOURS_LABELS, columns=INCOME_ORDER) * 100
    )
    n = stats["n"].unstack().reindex(index=HOURS_LABELS, columns=INCOME_ORDER).fillna(0)
    return rate, n


def full_data_range(step: int = 5) -> tuple[int, int]:
    """Droupout rate (%) range from the unfiltered data, rounded outward to `step` %. This is needed for the coloring of the heatmap. Computed once from the full dataset, so a color means the same rate under every filter, otherwise it would change with the filters."""
    rate, _ = hours_income_rates(df)
    lo = math.floor(rate.min().min() / step) * step
    hi = math.ceil(rate.max().max() / step) * step
    return lo, hi


HEATMAP_RANGE = full_data_range()


def hours_income_heatmap(d: pd.DataFrame) -> go.Figure:
    """Visualization for dropout rate by weekly work hours and family income"""
    if d.empty:
        return empty_figure("No students match the current filters")

    rate, n = hours_income_rates(d)
    labels = [
        ["" if pd.isna(v) else f"{v:.0f}%" for v in row_v] for row_v in rate.values
    ]

    fig = go.Figure(
        go.Heatmap(
            z=rate.values,
            x=INCOME_ORDER,
            y=HOURS_LABELS,
            text=labels,
            texttemplate="%{text}",
            customdata=n.values,
            zmin=HEATMAP_RANGE[0],
            zmax=HEATMAP_RANGE[1],
            colorscale="YlOrRd",
            xgap=2,
            ygap=2,
            hoverongaps=False,
            colorbar=dict(
                title=dict(text="Dropout %", side="right"), ticksuffix="%", thickness=12
            ),
            hovertemplate=(
                "<b>%{x} income | %{y} h/week</b><br>"
                "Dropout rate: %{z:.1f}%<br>"
                "Students: %{customdata:,}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        template="plotly_white",
        hoverlabel=HOVERLABEL,
        margin=dict(l=50, r=20, t=20, b=50),
        xaxis=dict(title="Family income"),
        yaxis=dict(title="Work hours / week"),
    )
    return fig
