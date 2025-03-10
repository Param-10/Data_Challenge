import os
import json
import time
import logging
import redis
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', 'influxdb')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', 'adminpassword')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'myorg')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'color_data')

class DataWorker:
    def __init__(self):
        # Redis connection
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        
        # InfluxDB connection
        self.influx_client = InfluxDBClient(
            url=f"http://{INFLUXDB_HOST}:8086", 
            token=INFLUXDB_TOKEN, 
            org=INFLUXDB_ORG
        )
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        
        # Color aggregation tracking
        self.color_data = {}
        self.aggregation_window = 60  # 1-minute aggregation window

    def process_message(self, message):
        try:
            data = json.loads(message)
            color = data.get('color')
            value = data.get('value')
            
            if color and value is not None:
                current_time = datetime.utcnow()
                
                # Aggregate data for this color
                if color not in self.color_data:
                    self.color_data[color] = {
                        'values': [],
                        'last_aggregation': current_time
                    }
                
                self.color_data[color]['values'].append(value)
                
                # Check if it's time to aggregate and write to InfluxDB
                if (current_time - self.color_data[color]['last_aggregation']).total_seconds() >= self.aggregation_window:
                    self.aggregate_and_write(color, current_time)
        
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON message: {message}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def aggregate_and_write(self, color, current_time):
        values = self.color_data[color]['values']
        
        # Calculate aggregates
        point = Point("color_metrics") \
            .tag("color", color) \
            .field("count", len(values)) \
            .field("mean", np.mean(values)) \
            .field("median", np.median(values)) \
            .field("min", np.min(values)) \
            .field("max", np.max(values)) \
            .time(current_time)
        
        # Write to InfluxDB
        self.write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        
        logger.info(f"Aggregated data for {color}: {point.to_line_protocol()}")
        
        # Reset color data
        self.color_data[color] = {
            'values': [],
            'last_aggregation': current_time
        }

    def run(self):
        logger.info("Worker started. Listening for messages...")
        
        try:
            # Subscribe to the color_data channel
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe('color_data')
            
            for message in pubsub.listen():
                if message['type'] == 'message':
                    self.process_message(message['data'])
        
        except Exception as e:
            logger.error(f"Error in worker: {e}")
        
        finally:
            self.influx_client.close()
            self.redis_client.close()

if __name__ == "__main__":
    worker = DataWorker()
    worker.run()