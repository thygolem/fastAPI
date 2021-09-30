# Siguiendo el tutorial: https://www.youtube.com/watch?v=iOZ28g2fe-U
# Siguiendo también el tutorial: https://www.youtube.com/watch?v=_eWEmRWhk9A

# Pymongo mejoras https://www.youtube.com/watch?v=KgedaDkrKoc&list=PLnLzwYW6HOC6aVYvO2O_GN_YU_r_ssowm&index=6

from typing import List, Optional, Text

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from uuid import uuid4 as uuid

app = FastAPI()

devicesData = []

class Device(BaseModel):
    id: Optional[str]
    esp_mac: str
    near_mac: Optional[str]
    rssi: Optional[int]
    building: Optional[str]
    floor: Optional[str]
    zone: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    task: Optional[bool]
    # característicasDeLaZona: List[str] que deben de ser añadidas como #tag y método .append() min 16:00

@app.get('/')
def api_root():
    return {'message': 'bienvenidx a sistemas Simó'}

@app.post("/device/")
def prepare_device(
    device: Device,
    #task: bool = Query(False, description="TAREA PENDIENTE EN ESTA ZONA (True/False)"),
):
    device.id = str(uuid())
    devicesData.append(device.dict())
    return {
        "message": f"{device.esp_mac} DETECTS {device.near_mac} RSSI={device.rssi} ZONA={device.building}/{device.floor}/{device.zone}TAREA={device.task}"
    }

@app.get('/devices/')
def read_devices():
    return devicesData

@app.get('/devices/{device_id}')
def read_device(device_id: str):
    for device in devicesData:
        if device['id'] == device_id:
            return device
    raise HTTPException(status_code=404, detail='Post not found')


@app.delete('/devices/{device_id}')
def delete_device(device_id: str):
    for index, device in enumerate(devicesData):
        if device['id'] == device_id:
            devicesData.pop(index)
            return {'message': 'Post deleted'}
    raise HTTPException(status_code=404, detail='Post not found')


@app.put('/devices/{device_id}')
def update_device(device_id: str, updatedDevice: Device):
    for index, device in enumerate(devicesData):
        if device['id'] == device_id:
            devicesData[index]['building'] = updatedDevice.building
            devicesData[index]['floor'] = updatedDevice.floor
            devicesData[index]['zone'] = updatedDevice.zone
            devicesData[index]['lat'] = updatedDevice.lat
            devicesData[index]['lng'] = updatedDevice.lng
            devicesData[index]['task'] = updatedDevice.task
            return {'message': 'Post updated'}
    raise HTTPException(status_code=404, detail='Post not found')