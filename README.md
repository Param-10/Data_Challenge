# Real-Time Color Data Processing Pipeline

## Overview
This project implements a real-time data processing pipeline that:
- Generates random color-based numerical data
- Processes and aggregates the data
- Stores data in InfluxDB
- Visualizes data in Grafana

## Components
- **Data Generator**: Produces random messages with colors and values
- **Worker**: Aggregates and stores data in InfluxDB
- **Redis**: Message bus for data transmission
- **InfluxDB**: Time-series database for storing aggregated metrics
- **Grafana**: Visualization dashboard

## Prerequisites
- Docker
- Docker Compose

## Setup and Running

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Environment Configuration
The project uses default configurations, but you can customize via environment variables in `docker-compose.yml`:
- `GENERATOR_INTERVAL`: Time between data generation (default: 1 second)
- Redis, InfluxDB, and Grafana have default credentials

### 3. Start the Pipeline
```bash
docker-compose up --build
```

### 4. Access Services
- **Grafana**: http://localhost:3000
  - Default Login: admin/adminpassword
- **Dashboard**: http://localhost:8050

## Grafana Dashboard Configuration
1. Log in to Grafana
2. Add InfluxDB as a data source
   - URL: http://influxdb:8086
   - Organization: myorg
   - Bucket: color_data
   - Token: adminpassword

### Recommended Grafana Panels
1. **Time Series**: Color Values Over Time
   - Measurement: color_metrics
   - Group by: color
   - Metrics: mean, median, min, max

2. **Stat Panels**: Current Color Statistics
   - Show latest mean and max values per color

## Customization
- Modify `data_generator.py` to change:
  - Colors
  - Value ranges
  - Generation interval

## Troubleshooting
- Check Docker logs for each service
- Ensure all services are running
- Verify network connectivity

## License
[Your License Here]