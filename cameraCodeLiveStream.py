import cv2
import numpy as np
import sys
import time
import imutils
from picamera import PiCamera
from picamera.array import PiRGBArray

#global variables
widthOfFrame = 0
heightOfFrame = 0
count = 0
enterCount = 0
exitCount = 0
idealContourSize = 9000         # Set contour size to choose which object to detect.
thresholdValue = 50             # Set threshold value for binarization.
refLineDistance = 35            # Distance from the center in pixels

#Check if an object is entering.
timer = 0
def checkEntry(yContour, yEntrance, yExit):
  absoluteDist = abs(yContour - yEntrance)
  if ((absoluteDist <= 1) and (yContour < yExit)):
      return 1
  else:
      return 0

#Check if an object in exiting.
def checkExit(yContour, yEntrance, yExit):
    absoluteDist = abs(yContour - yExit)
    if ((absoluteDist <= 1) and (yContour > yEntrance)):
        return 1
    else:
        return 0

# Pauses for 5 seconds.
def skipSomeFrames(cameraInput):
    time.sleep(5)

# Set the resolution of the raspberry pi camera to 680x480.
resX = 640
resY = 480
camera = PiCamera()
camera.resolution = (resX,resY)
cameraInput= PiRGBArray(camera,size=(resX,resY))

referenceFrame = None # Set the reference frame to detect any movement in the frame.

for frame in camera.capture_continuous(cameraInput, format="bgr", use_video_port=True):
    cameraInput.truncate(0) # clear the stream in preparation for the next frame
    frame = frame.array
    frame = imutils.resize(frame, width = 500)
    heightOfFrame = np.size(frame,0)
    widthOfFrame = np.size(frame,1)

    # gray-scale convertion and Gaussian blur filter applying
    grayScaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayScaled = cv2.GaussianBlur(grayScaled, (15, 15), 0)
    
    if referenceFrame is None:
        referenceFrame = grayScaled
        continue

    # Background subtraction and image binarization
    changeInFrame = cv2.absdiff(referenceFrame, grayScaled)
    frameThreshold = cv2.threshold(changeInFrame, thresholdValue, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Threshold frames", frameThreshold)
    # Dilate image and find all the contours
    frameThreshold = cv2.dilate(frameThreshold, None, iterations=1)
    contours= cv2.findContours(frameThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    numberOfContours = 0

    # plot reference lines (entrance and exit lines) 
    yEntrance = (heightOfFrame / 2)-refLineDistance
    yExit = (heightOfFrame / 2)+refLineDistance
    cv2.line(frame, (0,int(yEntrance)), (widthOfFrame,int(yEntrance)), (255, 0, 0), 2)
    cv2.line(frame, (0,int(yExit)), (widthOfFrame,int(yExit)), (0, 0, 255), 2)

    for c in contours:
        if cv2.contourArea(c) < idealContourSize: # All contous smaller than ideal contour are will be ignore.
            continue

        numberOfContours = numberOfContours+1    

        # draw a bounding box around the object.
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # find object's centroid
        xCentroid = int((x+x+w)/2)
        yCentroid = int((y+y+h)/2)
        centroid = (xCentroid,yCentroid)
        cv2.circle(frame, centroid, 1, (0, 0, 0), 5)
        
        if (checkEntry(yCentroid,yEntrance,yExit)):
            enterCount += 1
            
        if (checkExit(yCentroid,yEntrance,yExit)):  
            exitCount += 1

        count = enterCount - exitCount

        # Write entrance and exit counter values on frame and shows it
    cv2.putText(frame, "Entrances: {}".format(str(enterCount)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Exits: {}".format(str(exitCount)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if count < 0:
        count = 0
    cv2.putText(frame, "Count: {}".format(str(count)), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Original Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    

     # Program execution will stop once q is pressed.
    if key == ord("q"):
        sys.exit()

# cleanup the camera and close any open windows
cameraInput.release()
cv2.destroyAllWindows()