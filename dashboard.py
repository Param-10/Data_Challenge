from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB Configuration
bucket = "color_data"
org = "myorg"
token = "adminpassword"
url = "http://influxdb:8086"

# Create InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Initialize Dash app
app = Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1('Color Data Dashboard'),
    
    # Time series plot
    dcc.Graph(id='time-series-plot'),
    
    # Interval component to update the graph periodically
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the time series plot
@app.callback(
    Output('time-series-plot', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    # Query InfluxDB for color metrics
    query_api = client.query_api()
    query = f'''
    from(bucket:"{bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "color_metrics")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    '''
    
    result = query_api.query_data_frame(query)
    
    if result is not None and not result.empty:
        # Create a time series plot
        fig = px.line(result, x='_time', y=['red', 'green', 'blue'], 
                      title='Color Metrics Over Time',
                      labels={'_time': 'Time', 'value': 'Value'},
                      color_discrete_map={'red': 'red', 'green': 'green', 'blue': 'blue'})
        return fig
    else:
        # Return an empty figure if no data
        return px.line(title='No Data Available')

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)