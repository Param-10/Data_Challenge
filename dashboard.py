from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import influxdb_client
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import time

# InfluxDB Configuration
bucket = "color_data"
org = "myorg"
token = "h4TtaKhm5jxL4i0YjegFKSyZn0s0jgZakQ3TJB97FxiQIho_K1-Ae08oS4-BUpLd7hp4wAH0vULt3KUAA70T-w=="
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

@app.callback(
    Output('time-series-plot', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    # Query InfluxDB for color metrics
    query_api = client.query_api()
    query = '''
    from(bucket: "color_data")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "color_metrics")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> group(columns: ["color"])
    '''
    
    result = query_api.query(org=org, query=query)
    
    if result:
        # Convert the result to a DataFrame
        records = []
        for table in result:
            for record in table.records:
                records.append(record.values)
        
        df = pd.DataFrame(records)
        
        if not df.empty:
            # Convert _time to local timezone (America/New_York)
            df['_time'] = pd.to_datetime(df['_time'], utc=True).dt.tz_convert('America/New_York')

            # Create a time series plot
            fig = px.line(df, x='_time', y=['mean', 'median', 'min', 'max'],
                          title='Color Metrics Over Time',
                          labels={'_time': 'Local Time (America/New_York)', 'value': 'Value'},
                          color='color')
            return fig
        else:
            return px.line(title='No Data Available')
    else:
        return px.line(title='No Data Available')

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
