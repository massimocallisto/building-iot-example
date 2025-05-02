# Building IoT Management System

A FastAPI-based API for managing IoT devices in a building infrastructure.

## Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning the repository)

## Getting Started

### Running with Docker

1. Clone or download this repository (if you haven't already):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Make sure you have the following files in your project directory:
   - `main.py` (FastAPI application)
   - `Dockerfile`
   - `docker-compose.yml`
   - `requirements.txt`

3. Build and start the container:
   ```bash
   docker-compose up --build
   ```

   The API will be available at http://localhost:8000

4. To stop the application:
   ```bash
   docker-compose down
   ```

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `GET /building`: Get building information
- `GET /floors`: List all floors
- `GET /floor/{floor_id}`: Get specific floor details
- `GET /floor/{floor_id}/devices`: Get all devices on a specific floor
- `GET /floor/{floor_id}/device/{device_id}`: Get specific device details
- `POST /floor/{floor_id}/device`: Add a new device to a floor
- `PUT /floor/{floor_id}/device/{device_id}/telemetry`: Update device telemetry

## Device Types

The system supports two types of devices:
- `presence_sensor`
- `light_actuator`

## Development

To make changes to the code while the container is running, simply edit the files locally. The changes will be reflected in the container thanks to the volume mounting configuration in docker-compose.yml.