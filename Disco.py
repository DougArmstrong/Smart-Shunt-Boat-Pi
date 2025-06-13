import asyncio
from bleak import BleakClient

async def discover_services(device_address):
    async with BleakClient(device_address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid} - {characteristic.properties}")

loop = asyncio.get_event_loop()
loop.run_until_complete(discover_services("D8:6D:E4:5F:C5:C8"))
