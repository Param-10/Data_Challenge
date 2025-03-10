import json
import time
import redis
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import statistics

# InfluxDB configuration
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "your-influxdb-token"  # Change this to your actual token
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "data-pipeline"

# Time window for aggregation (in seconds)
AGGREGATION_WINDOW = 10

class DataAggregator:
    def __init__(self):
        # Connect to Redis
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        self.pubsub = self.redis_client.pubsub()
        
        # Connect to InfluxDB
        self.influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        
        # Data storage for aggregation
        self.data_by_color = {
            "red": [],
            "blue": [],
            "green": [],
            "yellow": []
        }
        
        # Last aggregation time
        self.last_aggregation_time = time.time()
    
    def process_message(self, message):
        """Process incoming messages from Redis."""
        if message['type'] == 'message':
            data = json.loads(message['data'])
            print(f"Received: {data}")
            
            # Add value to corresponding color list
            if data['color'] in self.data_by_color:
                self.data_by_color[data['color']].append(data['value'])
            
            # Check if it's time to aggregate
            current_time = time.time()
            if current_time - self.last_aggregation_time >= AGGREGATION_WINDOW:
                self.aggregate_and_store()
                self.last_aggregation_time = current_time
    
    def aggregate_and_store(self):
        """Aggregate data and store to InfluxDB."""
        current_time = datetime.utcnow()
        print(f"Aggregating data at {current_time}")
        
        for color, values in self.data_by_color.items():
            if values:
                # Calculate aggregations
                sum_value = sum(values)
                avg_value = statistics.mean(values)
                max_value = max(values)
                min_value = min(values)
                count = len(values)
                
                # Create InfluxDB point
                point = Point("color_metrics") \
                    .tag("color", color) \
                    .field("sum", sum_value) \
                    .field("avg", avg_value) \
                    .field("max", max_value) \
                    .field("min", min_value) \
                    .field("count", count) \
                    .time(current_time)
                
                # Write to InfluxDB
                self.write_api.write(bucket=INFLUXDB_BUCKET, record=point)
                
                print(f"Stored aggregation for {color}: Count={count}, Avg={avg_value:.2f}, Sum={sum_value}")
                
                # Clear data for next window
                self.data_by_color[color] = []
    
    def run(self):
        """Run the worker process."""
        # Subscribe to Redis channel
        self.pubsub.subscribe('data_channel')
        
        print("Worker started. Listening for messages...")
        
        try:
            for message in self.pubsub.listen():
                self.process_message(message)
        except KeyboardInterrupt:
            print("Worker stopped.")
        finally:
            self.pubsub.unsubscribe()
            self.influx_client.close()

if __name__ == "__main__":
    aggregator = DataAggregator()
    aggregator.run()