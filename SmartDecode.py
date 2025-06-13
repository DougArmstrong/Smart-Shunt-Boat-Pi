import asyncio
from bleak import BleakScanner, BleakClient

# Known UUIDs and their descriptions
uuid_info = {
    "6597ed8d-4bda-4c1e-af4b-551c4cf74769": "Voltage",
    "6597ed8c-4bda-4c1e-af4b-551c4cf74769": "Current",
    "6597ed8e-4bda-4c1e-af4b-551c4cf74769": "Power",
    "6597ed7d-4bda-4c1e-af4b-551c4cf74769": "AuxV"
    
    # Add other known UUIDs as needed
}

# Function to interpret the raw data based on length and context
def interpret_data(raw_data, uuid):
    if len(raw_data) == 2:  # U16
        value = int.from_bytes(raw_data, byteorder='little', signed=False)
    elif len(raw_data) == 4:  # S32 (current)
        value = int.from_bytes(raw_data, byteorder='little', signed=True) / 1000.0
    else:
        value = raw_data.hex()  # Unknown format, just display as hex
    return value

# Function to read and decode the characteristic
async def read_and_decode_characteristic(client, uuid, description):
    try:
        raw_data = await client.read_gatt_char(uuid)
        raw_data_hex = raw_data.hex()
        interpreted_value = interpret_data(raw_data, uuid)
        return raw_data_hex, interpreted_value
    except Exception as e:
        return "Error", str(e)

# Function to connect to the device and read all available characteristics
async def connect_and_read(device):
    async with BleakClient(device) as client:
        print(f"Connected to {device.name} [{device.address}]")

        services = await client.get_services()
        print(f"{'UUID':<40} | {'Content':<20} | {'Raw Data':<40} | {'Interpreted Value':<50}")
        print("-" * 150)

        for service in services:
            for characteristic in service.characteristics:
                uuid = characteristic.uuid
                description = uuid_info.get(uuid, "Unknown")
                raw_data, interpreted_value = await read_and_decode_characteristic(client, uuid, description)
                print(f"{uuid:<40} | {description:<20} | {raw_data:<40} | {interpreted_value:<50}")
            print("-" * 150)

async def main():
    print("Scanning for Bluetooth devices for 10 seconds...")
    devices = await BleakScanner.discover(timeout=10)

    selected_device = next((d for d in devices if d.name == 'SmartShunt HQ2148WZ4RP'), None)
    if selected_device is None:
        print("SmartShunt HQ2148WZ4RP not found.")
        return

    await connect_and_read(selected_device)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
