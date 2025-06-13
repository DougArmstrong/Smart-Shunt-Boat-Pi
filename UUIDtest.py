import asyncio
from bleak import BleakClient

async def read_characteristics(device_address):
    async with BleakClient(device_address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid} - {characteristic.properties}")
                
                # Attempt to read the characteristic if it supports reading
                if "read" in characteristic.properties:
                    try:
                        value = await client.read_gatt_char(characteristic.uuid)
                        print(f"    Value: {value}")
                    except Exception as e:
                        print(f"    Failed to read characteristic: {e}")

loop = asyncio.get_event_loop()
loop.run_until_complete(read_characteristics("D8:6D:E4:5F:C5:C8"))
import asyncio
from bleak import BleakClient

async def read_characteristics(device_address):
    async with BleakClient(device_address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid} - {characteristic.properties}")
                
                # Attempt to read the characteristic if it supports reading
                if "read" in characteristic.properties:
                    try:
                        value = await client.read_gatt_char(characteristic.uuid)
                        print(f"    Value: {value}")
                    except Exception as e:
                        print(f"    Failed to read characteristic: {e}")

loop = asyncio.get_event_loop()
loop.run_until_complete(read_characteristics("D8:6D:E4:5F:C5:C8"))
