const int LDR_PIN = A0;       // LDR connected to analog pin A0
const int THRESHOLD = 400;    // Light threshold for detecting 1 or 0 (adjust based on LDR sensitivity)
String binaryData = "";      // Store received binary data
int receivedBits = 0;        // Count bits
int consecutiveOnCount = 0;  // Count consecutive 1's (light ON)
bool transmissionStarted = false;  // Flag to indicate if transmission started

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud rate
  pinMode(LDR_PIN, INPUT);  // Set LDR pin as input
}

void loop() {
  int sensorValue = analogRead(LDR_PIN);  // Read the LDR light intensity
  
  // Check if the light is ON (value above threshold)
  if (sensorValue > THRESHOLD) {
    // If light is ON, treat it as '1'
    if (transmissionStarted) {
      binaryData += "1";  // Append 1 to binary data if transmission has started
      receivedBits++;
    }
    
    consecutiveOnCount++;  // Increase the count of consecutive '1's
  } else {
    // If light is OFF, treat it as '0'
    if (transmissionStarted) {
      binaryData += "0";  // Append 0 to binary data if transmission has started
      receivedBits++;
    }
    
    consecutiveOnCount = 0;  // Reset consecutive '1' count if light is OFF
  }

  // Check if we have received 8 consecutive '1's to start the transmission
  if (!transmissionStarted && consecutiveOnCount >= 8) {
    transmissionStarted = true;  // Start collecting binary data
    Serial.println("Transmission started!");  // Debug message
    consecutiveOnCount = 0;  // Reset consecutive '1' count
  }

  // Check if we have received 8 consecutive '1's to end the transmission
  if (transmissionStarted && consecutiveOnCount >= 8) {
    Serial.println("Transmission ended!");  // Debug message
    Serial.print("Received binary data: ");  // Show the received binary data
    Serial.println(binaryData);  // Send the collected data to the serial monitor
    // Reset everything for the next transmission cycle
    transmissionStarted = false;
    binaryData = "";  // Clear binary data
    receivedBits = 0;  // Reset received bits count
    consecutiveOnCount = 0;  // Reset consecutive '1' count
  }

  delay(100);  // Wait for 0.4 seconds before checking again
}
