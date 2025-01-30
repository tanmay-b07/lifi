Li-Fi Based File Transfer System

Project Overview
This project demonstrates a Li-Fi (Light Fidelity) based file transfer system, 
where data is transmitted using light instead of traditional radio waves. The system converts images into binary, modulates an LED to transmit the data,
and uses a photodiode on the receiver side to decode the information back into an image file.

Features
Wireless Data Transmission via visible light.
Image File Transfer Support.
Raspberry Pi as a Transmitter and Arduino as a Receiver.
Binary Encoding & Decoding for accurate data transfer.
Web Interface for user-friendly image selection and transmission.
Hardware Requirements
Raspberry Pi (Transmitter)
LED (For binary transmission)
Photodiode (Receiver)
Arduino (Receiver Processing)
Connecting wires & breadboard
Computer for image processing

Software Requirements
Python (For encoding and transmission)
Flask (For web interface)
Arduino IDE (For decoding and data reconstruction)
OpenCV (If image processing is required)

Working Principle
Image Input: An image file is uploaded via a web interface.
Binary Conversion: The image is converted into binary data.
Transmission via LED: The Raspberry Pi blinks an LED corresponding to the binary sequence (1 = ON, 0 = OFF).
Reception via Photodiode: The Arduino detects the blinking pattern and reconstructs the binary data.
Data Reconstruction: The received binary data is converted back into the original image file format.
Setup Instructions

1. Transmitter Side (Raspberry Pi)
Install dependencies: sudo apt install python3-flask
Run the web interface for image upload: python3 app.py
Convert the image to binary and transmit using LED.

2. Receiver Side (Arduino)
Upload the receiver code using Arduino IDE.
Connect the photodiode to Arduino and start capturing data.
Decode the received binary data and reconstruct the original image.
Future Improvements
Enhancing data transfer speed.
Supporting transmission of additional file types (videos, text, etc.).
Implementing error correction algorithms.

License
This project is open-source 
