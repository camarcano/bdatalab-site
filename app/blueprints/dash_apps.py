from flask import Blueprint
from dash import Dash, dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import datetime

# Define the main blueprint for all Dash apps
dash_bp = Blueprint('dash_bp', __name__, url_prefix='/dash')

# Sample data
data = {
    "Name": ["Max Scherzer", "Josh Hader", "Clayton Kershaw", "Emmanuel Clase", 
             "Blake Snell", "Devin Williams", "Gerrit Cole", "Edwin Diaz", 
             "Spencer Strider", "Ryan Helsley"],
    "G": [27, 61, 24, 75, 32, 68, 33, 64, 32, 58],
    "GS": [27, 0, 24, 0, 32, 0, 33, 0, 32, 0],
    "IP": [152.1, 56.2, 131.2, 72.1, 180.0, 58.2, 209.0, 62.0, 186.2, 54.1],
    "speX": [82.45, 85.92, 78.34, 89.76, 83.67, 86.23, 84.92, 88.45, 85.78, 87.34],
    "Barrel%": [6.8, 5.2, 7.4, 4.8, 5.9, 5.1, 6.2, 4.9, 5.7, 5.3],
    "SwStr%": [13.2, 16.8, 12.5, 15.4, 14.8, 17.2, 13.9, 16.5, 15.6, 15.8],
    "K-BB%": [22.4, 28.9, 19.8, 25.6, 24.2, 29.4, 23.8, 27.8, 26.2, 26.5],
    "CSW%": [31.2, 33.4, 30.1, 32.8, 31.5, 34.1, 31.8, 33.2, 32.4, 32.9],
    "pCRA": [3.2, 2.8, 3.5, 2.6, 3.1, 2.7, 3.0, 2.5, 2.9, 2.8],
    "O-Swing%": [33.5, 35.2, 32.8, 36.9, 34.1, 37.8, 33.9, 36.4, 35.2, 35.8],
    "Zone%": [42.8, 38.6, 43.5, 40.2, 41.3, 37.9, 42.1, 39.5, 40.8, 39.8],
    "Events": [421, 148, 362, 186, 486, 152, 568, 164, 498, 142],
    "Barrels": [18, 8, 21, 9, 24, 7, 28, 8, 26, 7],
    "Pitches": [2486, 892, 2124, 1086, 2892, 924, 3248, 968, 2986, 846],
    "CS": [428, 154, 386, 198, 492, 168, 586, 175, 524, 152],
    "Whiffs": [312, 168, 245, 184, 428, 178, 452, 182, 465, 164]
}
df = pd.DataFrame(data)

# Function to create a Dash app instance
def create_dash_app(flask_app, route_path, title, df):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=route_path,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # Define layout
    dash_app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3(title, className="text-center"),
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=datetime.date(2023, 1, 1),
                    max_date_allowed=datetime.date.today(),
                    initial_visible_month=datetime.date(2023, 1, 1),
                    start_date=datetime.date(2023, 1, 1),
                    end_date=datetime.date.today(),
                ),
                dbc.ButtonGroup([
                    dbc.Button("Season", id="btn-season"),
                    dbc.Button("Last 15 Days", id="btn-15d"),
                    dbc.Button("Last 30 Days", id="btn-30d"),
                    dbc.Button("Last Day", id="btn-1d"),
                ]),
                dbc.Input(id="min-ip", placeholder="Min IP", type="number", value=0.0),
                dbc.Button("Submit", id="submit-btn", color="primary", className="mt-2"),
                dbc.Button("Download CSV", id="download-btn", color="secondary", className="mt-2"),
            ], width=3),
            dbc.Col([
                html.Label("Select Players"),
                dbc.Textarea(id="player-select", placeholder="Enter player names, separated by commas"),
                dbc.Button("Clear Selection", id="clear-btn", color="warning", className="mt-2"),
                dbc.Label("Show entries"),
                dcc.Dropdown(
                    id="show-entries",
                    options=[{"label": str(i), "value": i} for i in ["All", 5, 10, 20, 50]],
                    value="All",
                    clearable=False,
                ),
                dbc.Input(id="search-input", placeholder="Search", type="text"),
            ], width=3),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id="player-table",
                    columns=[
                        {"name": col, "id": col, "deletable": False, "selectable": True, "hideable": True}
                        for col in df.columns
                    ],
                    data=df.to_dict("records"),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    page_action="none",
                    style_table={'overflowX': 'auto'},
                    style_header={'fontWeight': 'bold'},
                    style_cell={'textAlign': 'center'},
                ),
            ])
        ])
    ], fluid=True)

    # Callbacks for interactivity
    @dash_app.callback(
        Output("player-table", "data"),
        Input("submit-btn", "n_clicks"),
        State("player-select", "value"),
        State("min-ip", "value"),
        State("search-input", "value"),
        prevent_initial_call=True
    )
    def update_table(n_clicks, selected_players, min_ip, search_term):
        filtered_df = df.copy()
        
        # Apply player selection filter
        if selected_players:
            player_names = [name.strip() for name in selected_players.split(",")]
            filtered_df = filtered_df[filtered_df["Name"].isin(player_names)]
        
        # Apply minimum IP filter
        if min_ip:
            filtered_df = filtered_df[filtered_df["IP"] >= min_ip]
        
        # Apply search filter
        if search_term:
            filtered_df = filtered_df[filtered_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        
        return filtered_df.to_dict("records")

    @dash_app.callback(
        Output("player-table", "page_size"),
        Input("show-entries", "value")
    )
    def update_page_size(show_entries):
        return None if show_entries == "All" else int(show_entries)

    @dash_app.callback(
        Output("player-select", "value"),
        Input("clear-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_player_selection(n_clicks):
        return ""

    return dash_app

# Register the Dash apps with the Flask app
def init_dash_apps(flask_app):
    dash_app1 = create_dash_app(flask_app, "/dash/app1/", "Dash App 1", df)
    dash_app2 = create_dash_app(flask_app, "/dash/app2/", "Dash App 2", df)
