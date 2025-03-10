# Coding Challenge: Real-time Data Processing and Visualization Submission

## Overview
This project implements a real-time data pipeline as a submission for the "Real-time Data Processing and Visualization" coding challenge. The pipeline consists of three main components: a data generator, a worker, and a visualization dashboard.

1. **Data Generator**:  Generates random messages with color, name, and numerical value and publishes them to Redis Pub/Sub.
2. **Worker**: Subscribes to Redis Pub/Sub, aggregates the incoming messages, and stores the aggregated data in InfluxDB.
3. **Visualization Dashboard**: Uses Dash and Plotly to visualize the aggregated data from InfluxDB in real-time.

## Requirements
- **Scripting Language**: Python
- **Message Bus**: Redis Pub/Sub
- **Time Series Database**: InfluxDB
- **Visualization**: Dash, Plotly

## Project Components

### 1. Data Generator (`data_generator.py`)
- Generates random messages in JSON format:
  ```json
  {
    "color": "red",
    "name": "value_name",
    "value": 42
  }
  ```
- Publishes messages to Redis Pub/Sub at a regular interval (default: 1 second).
- Uses a predefined set of colors: "red", "blue", "green", "yellow".
- Generates numerical values within a random range: 1-100.

### 2. Worker (`worker.py`)
- Subscribes to Redis Pub/Sub.
- Aggregates numerical values by color, calculating mean, median, min, and max over a 5-second window.
- Stores the aggregated results in InfluxDB in the `color_data` bucket under the `color_metrics` measurement.

### 3. Visualization Dashboard (`dashboard.py`)
- Uses Dash and Plotly to create an interactive dashboard.
- Connects to InfluxDB to fetch aggregated color metrics.
- Plots time series data for mean, median, min, and max values for each color.
- Dashboard is accessible at http://localhost:8050.

## Setup and Running

### Prerequisites
- Docker: Ensure Docker is installed on your system.
- Docker Compose: Ensure Docker Compose is installed. You might need to install it separately depending on your Docker installation.

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <repository-name>
```
Replace `<your-repository-url>` and `<repository-name>` with the actual repository URL and name.

### 2. Start the Pipeline with Docker Compose
Navigate to the repository directory in your terminal. To start the pipeline, you can use either `docker-compose` or `docker compose`.

**Choose your command based on your Docker Compose installation:**

**Using `docker-compose` (with hyphen):**
```bash
docker-compose up --build
```

**Using `docker compose` (without hyphen):**
```bash
docker compose up --build
```

Run the chosen command in your terminal. This will:
- **Build**: Build Docker images for the dashboard, worker, and generator.
- **Start**: Launch all services: Redis, InfluxDB, Grafana, dashboard, worker, and generator.

This command will perform the following actions:

- **Build**: Build the Docker images for the `dashboard`, `worker`, and `generator` services as defined in the `docker-compose.yml` file.
- **Start**: Start all the services defined in `docker-compose.yml`, including `redis`, `influxdb`, `grafana`, `dashboard`, `worker`, and `generator`.

Wait for all services to start. You can check the logs in your terminal to monitor the startup process. Once all services are running, you can access the dashboard and Grafana.

### 3. Access Services

  **Generate a new InfluxDB API token (recommended):**
    1. Open your web browser and navigate to `http://localhost:8086` to access the InfluxDB UI.
    2. Log in to InfluxDB. - Default Login: admin/adminpassword
    3. Go to "API Tokens".
    4. Click "Generate API Token" and select "Custom Token".
    5. Give the token a name (e.g., "admin's token").
    6. Grant "Read" and "Write" permissions to the `color_data` bucket.
    7. Click "Save".
    8. Copy the generated API token.
    9. Replace the `token` value in `dashboard.py` and `data_generator.py` with your newly generated token.

- **Dashboard**: http://localhost:8050
  - Open your web browser and navigate to http://localhost:8050 to access the dashboard.

### Customization
- **Data Generation Interval**: Modify `GENERATOR_INTERVAL` environment variable in `docker-compose.yml` (default: 1 second).
- **InfluxDB Aggregation Window**: Adjust the time window in `worker.py` (currently 5 seconds).
- **Dashboard Update Interval**: Change `interval` in `dcc.Interval` in `dashboard.py` (currently 5 seconds).

### Troubleshooting
- **Check Docker Logs**: Use `docker-compose logs <service_name>` or `docker compose logs <service_name>` to check logs for each service (e.g., `docker-compose logs dashboard`).
- **Ensure Services are Running**: Use `docker-compose ps` or `docker compose ps` to verify all services are running.
- **Verify Network Connectivity**: Ensure Docker containers can communicate with each other.

## Bonus Features
- **Dockerized Components**: All components are containerized using Docker and orchestrated with Docker Compose.

## Submission Guidelines
- GitHub repository includes:
  - `data_generator.py`
  - `worker.py`
  - `dashboard.py`
  - `docker-compose.yml`
  - `requirements.txt`
  - `README.md` (this file)
  - `Dockerfile.generator`
  - `Dockerfile.worker`
  - `Dockerfile.dashboard`
  - `.gitignore`

Happy coding!
