from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from enum import Enum
from datetime import datetime

# Response Models
class MessageResponse(BaseModel):
    message: str

class DeviceType(str, Enum):
    PRESENCE_SENSOR = "presence_sensor"
    LIGHT_ACTUATOR = "light_actuator"

class Device(BaseModel):
    id: str
    type: DeviceType
    description: str
    telemetry: Dict[str, Any] = Field(default_factory=dict)

class Floor(BaseModel):
    id: str
    devices: List[Device] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "id": "Ground Floor"
            }
        }

class Building(BaseModel):
    name: str = ""
    floors: List[Floor] = Field(default_factory=list)
    address: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Office Building A",
                "address": "123 Main Street"
            }
        }

app = FastAPI(title="Building IoT Management")

# In-memory storage
building = Building(floors=[
    Floor(id="piano" + str(i)) for i in range(0, 15)
])

@app.get("/", response_model=MessageResponse)
async def root():
    return {"message": "Building IoT Management System"}

@app.get("/building", response_model=Building)
async def get_building():
    return building

@app.get("/floors", response_model=List[Floor])
async def get_floors():
    """Get all floors with their devices"""
    return building.floors

@app.get("/floor/{floor_id}", response_model=Floor)
async def get_floor(floor_id: str):
    """Get specific floor and its devices"""
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")
    else:
        return floor

@app.get("/floor/{floor_id}/devices", response_model=List[Device])
async def get_floor_devices(floor_id: str):
    """Get all devices on a specific floor"""
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")
    return floor.devices

@app.get("/floor/{floor_id}/device/{device_id}", response_model=Device)
async def get_device(floor_id: str, device_id: str):
    """Get a specific device by its ID on a specific floor"""
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")

    device = next((d for d in floor.devices if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.put("/floor/{floor_id}/device", response_model=Device)
async def add_device(floor_id: str, device_type: DeviceType, device_id: str, device_description: str):
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")
    # Check if device ID already exists
    if any(d.id == device_id for d in floor.devices):
        raise HTTPException(status_code=400, detail="Device ID already exists on this floor")
    new_device = Device(id=device_id, type=device_type, description=device_description)
    floor.devices.append(new_device)
    return new_device


@app.delete("/floor/{floor_id}/device/{device_id}", response_model=MessageResponse)
async def delete_device(floor_id: str, device_id: str):
    """Delete a specific device from a floor"""
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")
    device = next((d for d in floor.devices if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    floor.devices.remove(device)
    return {"message": f"Device {device_id} deleted successfully"}


@app.post("/floor/{floor_id}/device/{device_id}", response_model=Device)
async def update_device_description(floor_id: str, device_id: str, description: str):
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")
    device = next((d for d in floor.devices if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.description = description
    return device


@app.post("/floor/{floor_id}/telemetry/{device_id}", response_model=Device)
async def update_device_telemetry(floor_id: str, device_id: str, telemetry: Dict[str, Any]):
    floor = next((f for f in building.floors if f.id == floor_id), None)
    if not floor:
        raise HTTPException(status_code=400, detail="Invalid floor id")
    device = next((d for d in floor.devices if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.telemetry = telemetry
    return device

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)