import serial
import time

# Set your Arduino serial port (Windows: "COMx", Linux/Mac: "/dev/ttyUSBx" or "/dev/ttyACMx")
SERIAL_PORT = "COM3"  # Change as per your system
BAUD_RATE = 9600  
OUTPUT_BINARY_FILE = "received_binary.txt"
OUTPUT_IMAGE_FILE = "output_image.jpg"

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10)
time.sleep(2)  # Allow some time for connection

print("Waiting for data from Arduino...")

# Step 1: Read binary data from Arduino and save to file
with open(OUTPUT_BINARY_FILE, "w") as file:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if "Received Binary Data:" in line:
            binary_data = line.split(":")[1].strip()
            file.write(binary_data)
            print("Binary data saved to received_binary.txt")
            break  # Exit after receiving the data

ser.close()

# Step 2: Convert binary data back to an image
with open(OUTPUT_BINARY_FILE, "r") as file:
    binary_data = file.read().strip()

# Convert binary string to bytes
byte_data = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

# Save as an image
with open(OUTPUT_IMAGE_FILE, "wb") as img_file:
    img_file.write(byte_data)

print(f"Image reconstructed successfully as {OUTPUT_IMAGE_FILE}!")
