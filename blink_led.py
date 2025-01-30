import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 17  # Original LED pin
STARTING_LED_PIN = 27  # New starting LED pin (change this if necessary)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(STARTING_LED_PIN, GPIO.OUT)

# Turn on the starting LED before blinking the main LED
GPIO.output(STARTING_LED_PIN, GPIO.HIGH)
time.sleep(0.25)
GPIO.output(STARTING_LED_PIN, GPIO.LOW)
# Read the binary data from the file
with open('/rasp_file_path_here/binary_data.txt', 'r') as f:
    binary_data = f.read()

# Blink the LED according to the binary data
for bit in binary_data:
    if bit == '1':
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
    else:
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED
    time.sleep(0.25)  # Adjust the delay as needed

# After blinking ends, turn on the starting LED again
GPIO.output(STARTING_LED_PIN, GPIO.HIGH)
time.sleep(0.25)
GPIO.output(STARTING_LED_PIN, GPIO.LOW)

# Clean up GPIO
GPIO.cleanup()
