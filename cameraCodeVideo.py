import cv2
import numpy as np

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

# A function the skip some frames.
def skipSomeFrames(cameraInput):
    for i in range(0,20):
        (grabbed, frame) = cameraInput.read()

cameraInput = cv2.VideoCapture("video.mp4") # Take the video as an inout.

# Set the resolution to 680x480.
cameraInput.set(3,640)
cameraInput.set(4,480)

referenceFrame = None # Set the reference frame to detect any movement in the frame.

#The webcam maybe get some noise while starting up and apadting the brightness of the surrounding. So we skipp some initial frames.

skipSomeFrames(cameraInput) # Skip some initial frames to fetch only data only once camera settles down.

while True:
    (grabbed, frame) = cameraInput.read()    # grab frames one by one.
    if not grabbed:
        break
    heightOfFrame = np.size(frame,0)         # height of the frame.
    widthOfFrame = np.size(frame,1)          # width of the frame.

    # Covert the fram to gray-scale and use guassian blur.
    grayScaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayScaled = cv2.GaussianBlur(grayScaled, (15, 15), 0)
    
    if referenceFrame is None:
        referenceFrame = grayScaled         
        continue

    
    changeInFrame = cv2.absdiff(referenceFrame, grayScaled) # Check the difference between the reference and the current frame to know any activity.
    #Use binarization (values will be either 0 or 255) to remove background and make it all black, moving object will be white.
    frameThreshold = cv2.threshold(changeInFrame, thresholdValue, 255, cv2.THRESH_BINARY)[1] 
    cv2.imshow("Threshold frames", frameThreshold) # Show the threshol binarized video.
    frameThreshold = cv2.dilate(frameThreshold, None, iterations=1) #Dilate image and find all the contours.
    contours= cv2.findContours(frameThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # Save the contours in a variable.

    numberOfContours = 0

    # plot reference lines (entrance and exit lines) 
    yEntrance = (heightOfFrame / 2)-refLineDistance
    yExit = (heightOfFrame / 2)+refLineDistance
    cv2.line(frame, (0,int(yEntrance)), (widthOfFrame,int(yEntrance)), (255, 0, 0), 2)
    cv2.line(frame, (0,int(yExit)), (widthOfFrame,int(yExit)), (0, 0, 255), 2)

    # check all found countours
    for c in contours:
        if cv2.contourArea(c) < idealContourSize: # All contous smaller than ideal contour are will be ignore.
            continue

        numberOfContours = numberOfContours+1    

        # Draw bounding box around the object.
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

    # Show entrance and exit counters with actual count inside.
    cv2.putText(frame, "Entrances: {}".format(str(enterCount)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Exits: {}".format(str(exitCount)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if count < 0:
        count = 0
    cv2.putText(frame, "Count: {}".format(str(count)), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Original Frame", frame)
    key = cv2.waitKey(20) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"): 
        break
    

# cleanup the camera and close any open windows
cameraInput.release()
cv2.destroyAllWindows()