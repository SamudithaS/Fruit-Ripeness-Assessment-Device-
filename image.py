import serial
from PIL import Image
import numpy as np

# Configure the serial port (adjust the COM port as necessary)
ser = serial.Serial('COM3', 9600, timeout=1)  

# Define the size of the image (adjust based on your camera resolution)
width, height = 640, 480

# Define the file path where the image will be saved
save_path = 'D:\Samuditha UoC\Level III\Semester 1 Academics\PH3032 - Embedded Systems Laboratory\Final Project\Final\Images'

# Create an empty array to store the image data
image_data = []

print(f"Receiving image data...")

# Read the image data from UART
while True:
    data = ser.read(1024)  # Read 1024 bytes at a time
    if data:
        image_data.extend(data)
    else:
        break

ser.close()

# Convert the image data to a NumPy array
image_array = np.array(image_data, dtype=np.uint8)

# Ensure that the array length matches the expected image size
if len(image_array) == width * height:
    # Reshape the array into the correct format (2D array)
    image_array = image_array.reshape((height, width))

    # Convert the array to an image using Pillow
    img = Image.fromarray(image_array)

    # Save the image as a PNG
    img.save(save_path)
    print(f"Image saved at {save_path}")
else:
    print(f"Error: Received data does not match expected size of {width * height} pixels.")
