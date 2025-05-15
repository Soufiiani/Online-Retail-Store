import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load RFM data
rfm = pd.read_csv("rfm_customer_segments.csv")

# Check if required columns exist
expected_columns = {'Recency', 'Frequency', 'Monetary', 'Segment'}

missing = expected_columns - set(rfm.columns)

if missing:
    raise ValueError(f"Missing columns in CSV: {missing}")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Customer Segmentation Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Customer Segmentation (RFM)", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Recency', 'value': 'Recency'},
                {'label': 'Frequency', 'value': 'Frequency'},
                {'label': 'Monetary', 'value': 'Monetary'},
            ],
            value='Recency',
            clearable=False
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='bar-graph')
])


# Callback to update graph
@app.callback(
    Output('bar-graph', 'figure'),
    Input('metric-dropdown', 'value')
)
def update_graph(selected_metric):
    # Group and calculate averages
    cluster_summary = rfm.groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).reset_index().rename(columns={'CustomerID': 'Count'})


    # Create bar chart
    fig = px.bar(
        cluster_summary,
        x='Segment',
        y=selected_metric,
        color='Segment',
        title=f'Average {selected_metric} per Segment',
        text_auto='.2s'
    )

    fig.update_layout(transition_duration=500)
    return fig


# Run server
if __name__ == '__main__':
    app.run(debug=True)