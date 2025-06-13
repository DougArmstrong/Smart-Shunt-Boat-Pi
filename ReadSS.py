import bluetooth
import subprocess
import time

def reset_bluetooth():
    print("Resetting Bluetooth adapter...")
    subprocess.run(["sudo", "hciconfig", "hci0", "down"])
    time.sleep(1)  # Wait for a second
    subprocess.run(["sudo", "hciconfig", "hci0", "up"])
    time.sleep(2)  # Give it some time to settle
    print("Bluetooth adapter reset.")

def restart_bluetooth_service():
    print("Restarting Bluetooth service...")
    subprocess.run(["sudo", "systemctl", "restart", "bluetooth"])
    time.sleep(5)  # Give it some time to restart
    print("Bluetooth service restarted.")

# Reset Bluetooth and restart the service at the beginning
reset_bluetooth()
restart_bluetooth_service()

print("Creating Socket")
# Bluetooth setup
target_address = "D8:6D:E4:5F:C5:C8"  # Replace with your Smart Shunt's MAC address
port = 1  # This is commonly used for RFCOMM

try:
    # Create a Bluetooth socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    
    print("Longer Sleep.")
    time.sleep(10)  # Increase delay to 10 seconds before attempting to connect
    
    print(f"Connecting to {target_address}")
    sock.connect((target_address, port))
    print(f"Connected to {target_address}")

    while True:
        # Receive data from the Smart Shunt
        data = sock.recv(1024)  # Buffer size of 1024 bytes
        print("Received:", data.decode('utf-8'))  # Decode the bytes to a string

finally:
    # Clean up the connection
    sock.close()
    print("Connection closed.")
