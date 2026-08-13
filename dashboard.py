"""Interactive animal rescue dashboard backed by MongoDB."""

from __future__ import annotations

import os
from typing import Any

import dash_leaflet as dl
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, ctx, dash_table, dcc, html

from animal_shelter import AnimalShelter
from rescue_filters import build_rescue_query, classify_rescue_type


def records_frame(shelter: AnimalShelter, query: dict[str, Any] | None = None) -> pd.DataFrame:
    """Load MongoDB records into a dashboard-safe data frame."""
    frame = pd.DataFrame.from_records(shelter.read(query or {}))
    if "_id" in frame.columns:
        frame = frame.drop(columns=["_id"])
    return frame


def create_app(shelter: AnimalShelter) -> Dash:
    """Create the Dash application around an injected data layer."""
    app = Dash(__name__)
    initial_frame = records_frame(shelter)

    app.layout = html.Div(
        [
            html.H1("Animal Rescue Operations Dashboard"),
            html.P(
                "Filter candidate animals by rescue role, review the results, "
                "and select a record to inspect its location."
            ),
            dcc.RadioItems(
                id="filter-type",
                options=[
                    {"label": "Water Rescue", "value": "Water"},
                    {"label": "Mountain Rescue", "value": "Mountain"},
                    {
                        "label": "Disaster or Individual Tracking",
                        "value": "Disaster",
                    },
                ],
                value=None,
                inline=True,
            ),
            html.Button("Reset filters", id="reset-button", n_clicks=0),
            dash_table.DataTable(
                id="animal-table",
                columns=[{"name": column, "id": column} for column in initial_frame.columns],
                data=initial_frame.to_dict("records"),
                page_size=10,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="single",
                style_table={"overflowX": "auto"},
                style_cell={"padding": "6px", "textAlign": "left"},
            ),
            html.Div(
                [
                    html.Div(id="rescue-chart", style={"flex": "1"}),
                    html.Div(id="animal-map", style={"flex": "1"}),
                ],
                style={"display": "flex", "gap": "1rem", "flexWrap": "wrap"},
            ),
        ],
        style={"maxWidth": "1200px", "margin": "0 auto", "padding": "1rem"},
    )

    @app.callback(
        Output("animal-table", "data"),
        Output("filter-type", "value"),
        Input("filter-type", "value"),
        Input("reset-button", "n_clicks"),
    )
    def update_table(filter_type: str | None, reset_clicks: int) -> tuple[list[dict[str, Any]], str | None]:
        del reset_clicks
        if ctx.triggered_id == "reset-button":
            return initial_frame.to_dict("records"), None
        frame = records_frame(shelter, build_rescue_query(filter_type))
        return frame.to_dict("records"), filter_type

    @app.callback(
        Output("rescue-chart", "children"),
        Input("animal-table", "derived_virtual_data"),
    )
    def update_chart(records: list[dict[str, Any]] | None) -> Any:
        frame = pd.DataFrame(records or [])
        if frame.empty or "breed" not in frame.columns:
            return html.P("No chart data available.")
        frame["rescue_category"] = frame["breed"].apply(classify_rescue_type)
        figure = px.pie(
            frame,
            names="rescue_category",
            title="Animals by Rescue Category",
        )
        return dcc.Graph(figure=figure)

    @app.callback(
        Output("animal-map", "children"),
        Input("animal-table", "derived_virtual_data"),
        Input("animal-table", "derived_virtual_selected_rows"),
    )
    def update_map(
        records: list[dict[str, Any]] | None,
        selected_rows: list[int] | None,
    ) -> Any:
        if not records or not selected_rows:
            return html.P("Select an animal to view its location.")

        frame = pd.DataFrame(records)
        row_index = selected_rows[0]
        required = {"location_lat", "location_long", "breed", "name"}
        if row_index >= len(frame) or not required.issubset(frame.columns):
            return html.P("Location data is unavailable for this record.")

        row = frame.iloc[row_index]
        position = [row["location_lat"], row["location_long"]]
        return dl.Map(
            center=position,
            zoom=10,
            style={"width": "100%", "height": "500px"},
            children=[
                dl.TileLayer(),
                dl.Marker(
                    position=position,
                    children=[
                        dl.Tooltip(str(row["breed"])),
                        dl.Popup([html.Strong("Animal name"), html.P(str(row["name"]))]),
                    ],
                ),
            ],
        )

    return app


def main() -> None:
    """Load configuration, connect to MongoDB, and run the dashboard."""
    shelter = AnimalShelter(
        username=os.getenv("MONGODB_USERNAME"),
        password=os.getenv("MONGODB_PASSWORD"),
        host=os.getenv("MONGODB_HOST", "localhost"),
        database_name=os.getenv("MONGODB_DATABASE", "aac"),
        collection_name=os.getenv("MONGODB_COLLECTION", "animals"),
    )
    app = create_app(shelter)
    app.run(debug=os.getenv("DASH_DEBUG", "false").lower() == "true")


if __name__ == "__main__":
    main()
