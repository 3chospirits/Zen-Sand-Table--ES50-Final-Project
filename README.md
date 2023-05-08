# Zen Sand Table
### Team 18 - Edward Dan and Josh Freund

## Instructions for running code
To run code, the necessary packages in `requirements.txt` must be installed. We recommend installing these in a virtual environment. If you have python installed, you can set up a virtual environment and install packages by running these commands:

1) `python3 -m venv venv`
2) `source venv/bin/activate`
3) `pip install -r requirements.txt`

## Scripts
### Arduino
`control_scripts/calibrate/calibrate.ino` (calibrates) moves motors to 0,0

`control_scripts/joystick/joystick.ino` allows manual motor control via joystick

`control_scripts/step_motor/step_motor.ino` intercepts instructions from serial port (via computer) and moves each motor accordingly for computer generated drawings

### Python

`control_scripts/main.py` accepts input for gcode file and sends instructions to arduino to control motors using serial communication

`image_processing/image_processing.py` performs edge detection, erosion, dilation, and thinning on images. It will prompt users for a path to an image, an x, y pair for the size of a small structuring element, and an x, y pair for the size of a large structuring element. It outputs a processed image and images showing each intermediate processing step in a folder name "intermediates".

`image_processing/processed_to_coords.py` converts processed images to text files containing coordinates for the sand table. To run it, use `python3 processed_to_coords.py -i [path to image] -o [path to output file] -e white`.

`image_processing/constants.py` contains constants used in `processed_to_coords.py` (not executable)

`coordinates/offset_coords.py` offsets coordinates in a text file if it contains negative coordinates.
