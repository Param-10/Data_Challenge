# Coding Challenge: Real-time Data Processing and Visualization

## Overview
In this challenge, you will create a real-time data pipeline consisting of three components:

1. **Data Generator**: A script that generates random messages containing a color, name and a numerical value, then publishes them to a message bus.
2. **Worker**: A script that subscribes to the message bus, processes the incoming messages, and stores aggregated numerical data into a time series database.
3. **Visualization Dashboard**: A tool to visualize the aggregated data stored in the time series database.

## Requirements
- Use Python for scripting.
- Use Kafka, Redis Pub/Sub, or RabbitMQ as the message bus.
- Use InfluxDB, TimescaleDB, or Prometheus as the time series database.
- Use Grafana, Plotly, or Matplotlib for visualization.

## Part 1: Data Generator
Write a script that:
- Generates random messages in the format:
  ```json
  {
    "color": "red",
    "value": 42
  }
  ```
- Publishes these messages to a message bus at a regular interval (e.g., every second).
- Uses a set of predefined colors (e.g., "red", "blue", "green", "yellow").
- Generates numerical values within a random range (e.g., 1-100).

## Part 2: Worker
Write a script that:
- Subscribes to the message bus.
- Aggregates numerical values by color (e.g., sum, average) over a time window.
- Stores the aggregated results into a time series database.

## Part 3: Visualization Dashboard
- Use Grafana or another visualization tool to create a dashboard.
- Connect it to the time series database and plot the aggregated numerical values over time.
- Group data by color to visualize trends.

## Bonus
- Implement a streaming aggregation instead of storing raw values (e.g., calculate running averages).
- Add real-time alerts when a color’s value exceeds a threshold.
- Use Docker to containerize all components.

## Submission Guidelines
- Provide a GitHub repository with:
  - `data_generator.py`
  - `worker.py`
  - Instructions to set up the message bus, time series database, and visualization tool.
- Include a `README.md` with setup instructions.

Happy coding!
