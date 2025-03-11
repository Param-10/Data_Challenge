import os
import json
import time
import random
import logging
import redis
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
COLORS = ['blue', 'green', 'red', 'yellow']
INTERVAL = float(os.getenv('GENERATOR_INTERVAL', 1.0))  # seconds between messages
VALUE_RANGE = (1, 100)  # range of random values
TIMEZONE = os.getenv('TIMEZONE', 'America/New_York')  # Set your local timezone

class DataGenerator:
    def __init__(self):
        # Redis connection
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")

    def generate_message(self):
        """Generate a random message with color and value"""
        color = random.choice(COLORS)
        value = random.randint(*VALUE_RANGE)
        
        local_tz = pytz.timezone(TIMEZONE)
        timestamp = datetime.now(local_tz).isoformat()  # Use local time with timezone
        
        message = {
            'timestamp': timestamp,
            'color': color,
            'value': value
        }
        
        return message

    def run(self):
        logger.info("Data Generator started. Generating messages...")
        
        try:
            while True:
                # Generate and publish message
                message = self.generate_message()
                self.redis_client.publish('color_data', json.dumps(message))
                
                logger.info(f"Published message: {message}")
                
                # Wait before next message
                time.sleep(INTERVAL)
        
        except Exception as e:
            logger.error(f"Error in data generator: {e}")
        
        finally:
            self.redis_client.close()

if __name__ == "__main__":
    generator = DataGenerator()
    generator.run()
