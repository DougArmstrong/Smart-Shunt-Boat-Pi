import asyncio
from bleak import BleakScanner

async def run():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    if not devices:
        print("No devices found.")
    else:
        for device in devices:
            print(f"Found: {device.name} [{device.address}]")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
