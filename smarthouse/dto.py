from __future__ import annotations
from typing import Literal

from pydantic import BaseModel
from smarthouse.domain import Actuator, ActuatorWithSensor, Device, Floor, Room, Sensor, SmartHouse

"""
Classes for data transfer in the cloud service API endpoints between
what is sent/received int eh API and the data stored in the object structure
representing the smart house using the underlying domain model
"""

class SmartHouseInfo(BaseModel):

    no_rooms: int
    no_floors: int
    total_area: float
    no_devices: int

    @staticmethod
    def from_obj(house: SmartHouse) -> SmartHouseInfo:
        return SmartHouseInfo(
            no_rooms=len(house.get_rooms()),
            no_floors=len(house.get_floors()),
            total_area=house.get_area(),
            no_devices=len(house.get_devices()))


class FloorInfo(BaseModel):

    fid: int
    rooms: list[int]

    @staticmethod
    def from_obj(floor: Floor) -> FloorInfo:
        return FloorInfo(
            fid=floor.level,
            rooms=[r.rid for r in floor.rooms]
        )

class RoomInfo(BaseModel):

    rid: int | None
    room_size: float
    room_name: str | None
    floor: int
    devices: list[str]

    @staticmethod
    def from_obj(room: Room) -> RoomInfo:

        # Fordi devices er en kun liste med str, velger jeg å hente device-id (som er en unik
        # identifikator) fremfor device_name eller device_type. Dersom mere info skal være med her
        # skulle listen vært en liste med dto-objekter og ikke strenger. 

        devices = []    
        for d in room.devices:
            devices.append(d.id)

        # Alternativt:
        # for i in range (len(room.devices)):
        #     devices.append(room.devices[i].id)

        return RoomInfo(rid=room.rid, room_size=room.room_size, room_name=room.room_name, 
                        floor=room.floor.level, devices=devices)

class DeviceInfo(BaseModel):

    id: str
    model_name: str
    supplier: str
    device_type: str

    @staticmethod
    def from_obj(device: Device) -> DeviceInfo:
        return DeviceInfo(id=device.id, model_name=device.model_name, 
                          supplier=device.supplier, device_type=device.device_type)

class ActuatorStateInfo(BaseModel):

    # Dette er et objekt med èn attributt (str), ingen metoder
    state: str
