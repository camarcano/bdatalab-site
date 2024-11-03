# /routes/dash.py
from flask import Blueprint
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
from flask import current_app

# Create Blueprint
dash_blueprint = Blueprint('dash', __name__)

# Initialize the Dash app
def init_dash(server):
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dash/',
        assets_folder=current_app.static_folder,
        assets_url_path='/static/'
    )
    
    # Layout with both table and chart options
    dash_app.layout = html.Div([
        html.H1('Data Visualization Dashboard'),
        
        # Visualization type selector
        dcc.RadioItems(
            id='viz-type',
            options=[
                {'label': 'Table View', 'value': 'table'},
                {'label': 'Chart View', 'value': 'chart'}
            ],
            value='table',
            className='mb-4'
        ),
        
        # Container for the selected visualization
        html.Div(id='visualization-container'),
        
        # Chart type selector (only visible when chart is selected)
        html.Div([
            dcc.Dropdown(
                id='chart-type',
                options=[
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Scatter Plot', 'value': 'scatter'}
                ],
                value='line',
                className='mb-4'
            )
        ], id='chart-controls', style={'display': 'none'})
    ])
    
    @dash_app.callback(
        [Output('visualization-container', 'children'),
         Output('chart-controls', 'style')],
        [Input('viz-type', 'value'),
         Input('chart-type', 'value')]
    )
    def update_visualization(viz_type, chart_type):
        # This is where you would normally get your dataframe
        # For demonstration, we'll create a sample one
        df = pd.DataFrame({
            'Date': ['2024-01', '2024-02', '2024-03'],
            'Sales': [100, 120, 90],
            'Profit': [20, 25, 15]
        })
        
        if viz_type == 'table':
            return [
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                ),
                {'display': 'none'}
            ]
        
        else:  # chart view
            if chart_type == 'line':
                figure = {
                    'data': [
                        {'x': df['Date'], 'y': df['Sales'], 'type': 'line', 'name': 'Sales'},
                        {'x': df['Date'], 'y': df['Profit'], 'type': 'line', 'name': 'Profit'}
                    ],
                    'layout': {'title': 'Sales and Profit Over Time'}
                }
            elif chart_type == 'bar':
                figure = {
                    'data': [
                        {'x': df['Date'], 'y': df['Sales'], 'type': 'bar', 'name': 'Sales'},
                        {'x': df['Date'], 'y': df['Profit'], 'type': 'bar', 'name': 'Profit'}
                    ],
                    'layout': {'title': 'Sales and Profit Comparison'}
                }
            else:  # scatter
                figure = {
                    'data': [
                        {'x': df['Sales'], 'y': df['Profit'], 'type': 'scatter', 'mode': 'markers'}
                    ],
                    'layout': {'title': 'Sales vs Profit'}
                }
                
            return [dcc.Graph(figure=figure), {'display': 'block'}]
    
    return dash_app

# Blueprint route
@dash_blueprint.route('/dash')
def dash_page():
    return 'This route is not directly accessed'