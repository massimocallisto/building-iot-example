# Building IoT Management System

A FastAPI-based REST API for managing IoT devices in a building. The system allows you to manage devices across different floors in an open space layout.

## Google Docs fiel per ripartizione piani
https://docs.google.com/spreadsheets/d/1syRAWjqPiGaL4PPioYeZfwIz0RsDVU3RtZWYAlFo9Ws/edit?gid=0#gid=0

## IP dinamico del server in ascolto delle REST API
http://146.190.206.106:8185/

## Features

- Floor management
- Device management (sensors and actuators)
- Telemetry data handling
- Persistent storage using JSON file
- RESTful API design

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

## Running with Docker

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

### Root
- `GET /`
  - Returns a welcome message
  - Response Type: `MessageResponse`
  ```json
  {
      "message": "string"  
  }
  ```
  - Example Response:
  ```json
  {
      "message": "Building IoT Management System"
  }
  ```

### Building Management
- `GET /building`
  - Get building information including all floors and devices
  - Response Type: `Building`
  ```json
  {
    "name": "string",
    "floors": [
      {
        "id": "string",
        "devices": [
          {
            "id": "string",
            "type": "presence_sensor",
            "description": "string",
            "telemetry": {}
          }
        ]
      }
    ],
    "address": "string"
  }

### Floor Management
- `GET /floors`
  - Get all floors with their devices
  - Response Type: `Array<Floor>`
  ```json
  [
    {
      "id": "string",
      "devices": [
        {
          "id": "string",
          "type": "presence_sensor",
          "description": "string",
          "telemetry": {}
        }
      ]
    }
  ]
  ```


- `GET /floor/{floor_id}`
  - Get specific floor and its devices
  - Path Parameter: `floor_id` (string)
  - Response Type: `Floor`
  - Error: 400 if floor not found
  ```json
  {
    "id": "string",
    "devices": [
      {
        "id": "string",
        "type": "presence_sensor",
        "description": "string",
        "telemetry": {}
      }
    ]
  }
  ```

### Device Management
- `GET /floor/{floor_id}/devices`
  - Get all devices on a specific floor
  - Path Parameter: `floor_id` (string)
  - Response Type: `Array<Device>`
  - Error: 400 if floor not found
  ```json
  [
    {
      "id": "string",
      "type": "presence_sensor",
      "description": "string",
      "telemetry": {}
    }
  ]
  ```


- `GET /floor/{floor_id}/device/{device_id}`
  - Get a specific device on a floor
  - Path Parameters:
    - `floor_id` (string)
    - `device_id` (string)
  - Response Type: `Device`
  - Errors:
    - 400 if floor not found
    - 404 if device not found
  ```json
  {
    "id": "string",
    "type": "presence_sensor",
    "description": "string",
    "telemetry": {}
  }
  ```


- `POST /floor/{floor_id}/device`
  - Add a new device to a floor
  - Path Parameter: `floor_id` (string)
  - Query Parameters:
    - `device_type` (DeviceType: "presence_sensor" | "light_actuator")
    - `device_id` (string)
  - Response Type: `Device`
  - Errors:
    - 400 if floor not found
    - 400 if device ID already exists
  ```json
  {
    "id": "string",
    "type": "presence_sensor",
    "description": "string",
    "telemetry": {}
  }
  ```

- `PUT /floor/{floor_id}/device/{device_id}/telemetry`
  - Update device telemetry data
  - Path Parameters:
    - `floor_id` (string)
    - `device_id` (string)
  - Request Body: JSON object with telemetry data
    ```json
    {
        "device_id" : "pir75",
        "device_type" : "presence_sensor",
        "fw_version" : "1..0.1",
        "presence_status": true,
        "timestamp": "2023-10-25T14:30:00Z",
        "battery_level" : 3.6
    }
    ```
  - Response Type: `Device`
  - Errors:
    - 400 if floor not found
    - 404 if device not found

## Device Types
The system supports the following device types (enum `DeviceType`):
- `presence_sensor`
- `light_actuator`

## Development

To make changes to the code while the container is running, simply edit the files locally. The changes will be reflected in the container thanks to the volume mounting configuration in docker-compose.yml.

## Data Storage

The application uses in-memory storage and initializes with 5 empty floors (IDs: "1" through "5"). Data will be reset when the application restarts.
