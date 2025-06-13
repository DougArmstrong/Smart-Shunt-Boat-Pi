import asyncio
from bleak import BleakScanner, BleakClient

# Function to scan for devices
async def scan_devices():
    print("Scanning for Bluetooth devices for 10 seconds...")
    devices = await BleakScanner.discover(timeout=10)
    if not devices:
        print("No devices found.")
        return []
    else:
        print(f"Found {len(devices)} devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name} [{device.address}]")
        return devices

# Function to connect to a device and read characteristics
async def connect_and_read(device):
    async with BleakClient(device) as client:
        print(f"Connected to {device.name} [{device.address}]")

        # Assuming the device has characteristics for voltage, current, and power
        # Replace these UUIDs with the actual characteristic UUIDs from your Smart Shunt
        try:
            voltage = await client.read_gatt_char("uuid-for-voltage-characteristic")
            current = await client.read_gatt_char("uuid-for-current-characteristic")
            power = await client.read_gatt_char("uuid-for-power-characteristic")

            print(f"Voltage: {int.from_bytes(voltage, byteorder='little') / 1000} V")
            print(f"Current: {int.from_bytes(current, byteorder='little') / 1000} A")
            print(f"Power: {int.from_bytes(power, byteorder='little')} W")
        except Exception as e:
            print(f"Failed to read characteristics: {e}")

async def main():
    devices = await scan_devices()
    if not devices:
        return

    # Let the user select a device
    device_index = int(input("Select a device by index: "))
    if device_index < 0 or device_index >= len(devices):
        print("Invalid selection.")
        return

    selected_device = devices[device_index]
    await connect_and_read(selected_device)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
