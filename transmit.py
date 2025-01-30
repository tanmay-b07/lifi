import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import paramiko
from PIL import Image

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key' 

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert the black-and-white image to binary (0 for black, 1 for white)
def file_to_binary(filepath):
    image = Image.open(filepath).convert('1')  # Convert image to black-and-white (1-bit)
    binary_string = '11111111'  # Start sequence (8 ones)
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            # 255 is white, 0 is black
            binary_string += '1' if pixel == 255 else '0'
    binary_string += '11111111'  # End sequence (8 ones)
    return binary_string

# Transfer the text file to Raspberry Pi and execute LED blink code
def transfer_to_raspberry(binary_data):
    pi_host = "Host_name"  # Use the Raspberry Pi's IP address if needed
    pi_user = "user_name"
    pi_password = "pass"  # Hardcoded Raspberry Pi password

    try:
        # Create SSH client and connect to Raspberry Pi using password authentication
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(pi_host, username=pi_user, password=pi_password)

        # Save binary data to a file on Raspberry Pi
        sftp = ssh.open_sftp()
        with sftp.open('/rasp_file_path_here/binary_data.txt', 'w') as remote_file:
            remote_file.write(binary_data)  # Transfer the binary data
        sftp.close()

        # Execute the LED blink script on Raspberry Pi
        stdin, stdout, stderr = ssh.exec_command('/rasp_file_path_here/blink_led.py')
        stdout.channel.recv_exit_status()  # Wait for the script to finish
        # ssh.close()
    except Exception as e:
        return f"Error during transmission: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Convert the image to binary (0 and 1)
            binary_data = file_to_binary(filepath)

            # Save binary data to a text file
            text_file = os.path.join(app.config['UPLOAD_FOLDER'], 'binary_data.txt')
            with open(text_file, 'w') as f:
                f.write(binary_data)

            # Debugging: Check if the file was created successfully
            if os.path.exists(text_file):
                flash('File converted to binary! Now you can transmit it to the Raspberry Pi.')
            else:
                flash('Failed to create binary data file.')

            return render_template('index.html', transmit_file=text_file)

    return render_template('index.html')

@app.route('/transmit', methods=['POST'])
def transmit_file():
    if request.method == 'POST':
        text_file = os.path.join(app.config['UPLOAD_FOLDER'], 'binary_data.txt')

        if not os.path.exists(text_file):
            flash('No text file to transmit. Upload a file first.')
            return redirect(url_for('upload_file'))

        try:
            binary_data = open(text_file, 'r').read()  # Read binary data from the text file
            # Show the message: "File transmitted and LED Blink started!"
            flash('File transmitted and LED Blink started!')  # Message after transmission

            transfer_to_raspberry(binary_data)  # Transfer the binary data to Raspberry Pi

            # After completion of the LED blink, show the message
            flash('Transmission ended!')  # Final message after completion
        except Exception as e:
            flash(f'Error during transmission: {e}')  # Error message
    
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
