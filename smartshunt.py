import asyncio
from bleak import BleakScanner, BleakClient
import requests
import os

# Your Node-RED endpoint URL
node_red_url = "http://pi.boat:1880/ShorePower"

# Known UUIDs and their descriptions
uuid_info = {
    "6597ed8d-4bda-4c1e-af4b-551c4cf74769": "Voltage",
    "6597ed8c-4bda-4c1e-af4b-551c4cf74769": "Current",
    "6597ed8e-4bda-4c1e-af4b-551c4cf74769": "Power",
    "6597ed7d-4bda-4c1e-af4b-551c4cf74769": "12V_Battery"
}

# UUID for the keep-alive characteristic
keep_alive_uuid = "6597ffff-4bda-4c1e-af4b-551c4cf74769"

# Function to send the keep-alive signal
async def send_keep_alive(client):
 
    try:
        await client.write_gatt_char(keep_alive_uuid, bytearray([0xFF, 0xFF]))
        print("Keep-alive sent")
    except Exception as e:
        print(f"Failed to send keep-alive: {e}")

# Function to interpret and send data
def send_to_node_red(data):
    try:
        response = requests.post(node_red_url, json=data)
        print(f"Data sent: {data}, Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")

# Function to interpret the raw data based on length and context
def interpret_data(raw_data, uuid):
    if len(raw_data) == 2:  # U16 or S16
        value = int.from_bytes(raw_data, byteorder='little', signed=True) / 100.0
    elif len(raw_data) == 4:  # S32 (current)
        value = int.from_bytes(raw_data, byteorder='little', signed=True) / 1000.0
    else:
        value = raw_data.hex()  # Unknown format, just display as hex
    return value

# Function to read and decode the characteristic
async def read_and_decode_characteristic(client, uuid, description):
    try:
        raw_data = await client.read_gatt_char(uuid)
        interpreted_value = interpret_data(raw_data, uuid)
        return interpreted_value
    except Exception as e:
        return f"Error: {str(e)}"

# Function to connect to the device and read the characteristics
async def connect_and_display(device):
    tCount = 0
    client = None
    
    while True:
        try:
            # Ensure connection is established
            if client is None or not client.is_connected:
                client = BleakClient(device)
                await client.connect()
                print(f"Connected to {device.name} [{device.address}]")

            os.system('clear')  # Clear the terminal for a nice display
            print(f"{'UUID':<40} | {'Content':<10} | {'Value':<20}")
            print("-" * 80)
                    
            data = {}
            for uuid, description in uuid_info.items():
                interpreted_value = await read_and_decode_characteristic(client, uuid, description)
                data[description] = interpreted_value
                print(f"{uuid:<40} | {description:<10} | {interpreted_value:<20}")

            tCount += 1
            print(f"Count= {tCount} ")
            send_to_node_red(data)
            await send_keep_alive(client)  # Ensure keep-alive is sent
            await asyncio.sleep(6)  # Refresh every 6 seconds

        except Exception as e:
            print(f"Disconnected or error occurred: {e}. Attempting to reconnect...")
            tCount = 0
            client = None  # Reset client to trigger reconnection
            await asyncio.sleep(3)  # Wait before retrying connection

async def main():
    while True:
        try:
            print("Scanning for Bluetooth devices...")
            devices = await BleakScanner.discover(timeout=10)

            selected_device = next((d for d in devices if d.name == 'SmartShunt HQ2148WZ4RP'), None)
            if selected_device is None:
                print("SmartShunt HQ2148WZ4RP not found. Retrying in 10 seconds...")
                await asyncio.sleep(10)
                continue

            await connect_and_display(selected_device)
        except Exception as e:
            print(f"Failed to connect: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
