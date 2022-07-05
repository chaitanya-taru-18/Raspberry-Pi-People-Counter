# Raspberry-Pi-People-Counter

# IoT Device

## Building the device
### Requirements
1. Raspberry Pi 4 Computer Model B 4GB RAM
2. Pi Camera

### Required packages
cv2, imutils, math, numpy, picamera.

### Connections
Connect Pi camera to the camera module port in raspberry Pi (<i>refer</i> - https://projects.raspberrypi.org/en/projects/getting-started-with-picamera).

## Installation
Onto the ceiling, close to the room door, with the camera facing the region where people have to cross through for entering and exiting a room.

### cameraCodeVideo.py
Reading the recorded video and processing the count of people inside the room (by calculating the number of people who have entered and exited) is done in this file.
The attributes in the file are needed to be tuned according to the area, ambience, angle, distance, and frame size of the camera.

### cameraCodeLiveStream.py
Reading the livestream video and processing the count of people inside the room (by calculating the number of people who have entered and exited) is done in this file.
The attributes in the file are needed to be tuned according to the area, ambience, angle, distance, and frame size of the camera.

## Video Information
### video.mp4 
This is used by cameraCodeVideo.py as input.

### preprocessed.mp4
This is recorded during the execution of cameraCodeVideo.py. This is preprocessed version of video.mp4.

### outputVideo.mp4
This is recorded during the execution of cameraCodeVideo.py. By watching this video one can understand how this code works.
