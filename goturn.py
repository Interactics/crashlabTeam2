#!/usr/bin/env python
# Copyright 2018 Satya Mallick (LearnOpenCV.com)
 
# Import modules
import cv2, sys, os
import time

time.sleep(10)
### Code for Goturn

# if not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
#     errorMsg = '''
#     Could not find GOTURN model in current directory.
#     Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
#     '''
 
#     print(errorMsg)
#     sys.exit()

##############
 
# Create tracker
tracker = cv2.TrackerTLD_create()
 
# Read video
video = cv2.VideoCapture(3)
video.set(3,320)
video.set(4,240)

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()
 
# Read first frame
ok, frame = video.read()
if not ok:
    print("Cannot read video file")
    sys.exit()
 
# Define a bounding box
#bbox = (20, 23, 86, 100)
 
# Uncomment the line below to select a different bounding box

##bbox = cv2.selectROI(frame, False)
 
# Initialize tracker with first frame and bounding box
##ok = tracker.init(frame, bbox)
#flg =0
#tie =0
while True:
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break
 
    # Start timer

    timer = cv2.getTickCount()
    #tie=+tie+1
    ##print tie

    if(tie >30 and flg ==0) :
        bbox = cv2.selectROI(frame, False)
        ok = tracker.init(frame, bbox)
        flg = 1

    # Update tracker
    ok, bbox = tracker.update(frame)
 
    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
 
    # Display tracker type on frame
    cv2.putText(frame, "GOTURN Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
 
    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
 
    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
