from flask import Blueprint
from dash import Dash
from dash import html, dcc, dash_table

# Define the main blueprint for all Dash apps
dash_bp = Blueprint('dash_bp', __name__, url_prefix='/dash')

# Function to create a Dash app instance
def create_dash_app(flask_app, route_path, title, df=None):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=route_path,
        suppress_callback_exceptions=True
    )

    # Sample layout; customize as needed based on the DataFrame
    dash_app.layout = html.Div([
        html.H1(title),
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns] if df is not None else [],
            data=df.to_dict('records') if df is not None else [],
            editable=True,
            filter_action="native",
            sort_action="native",
            page_size=5
        ),
        dcc.Graph(
            figure={
                "data": [
                    {"x": df['Category'], "y": df['Value'], "type": "bar", "name": title}
                ],
                "layout": {"title": title}
            }
        ) if df is not None else html.Div("No data available.")
    ])

    return dash_app

# Register multiple Dash apps with unique routes
def init_dash_apps(flask_app):
    df1 = {
        "Category": ["A", "B", "C"],
        "Value": [10, 20, 30]
    }  # Replace this with your actual DataFrame

    dash_app1 = create_dash_app(flask_app, "/dash/app1/", "Dash App 1", df1)
    dash_app2 = create_dash_app(flask_app, "/dash/app2/", "Dash App 2", df1)
