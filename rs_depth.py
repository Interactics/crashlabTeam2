#!/usr/bin/env python

# This node for Target Selection 
# SUB Depth, boudning box 
# PUB selected person's Bounding BOX 
#- /camera/color/image_raw

##########################

##########################

##########################

#import ros
import pyrealsense2 as rs
import numpy as np
import cv2
import math

def getVerticalCoordinate(y,distance):
    # realsense RGB : FOV 60.4 x 42.5 x 77 (H V D)
    # realsense Depth : FOV 73 x 58 x 95 (H V D)
    VFov2 = math.radians(42.5 / 2)
    VSize = math.tan(VFov2) * 2
    Vcenter = (height -1 ) /2 
    VPixel = VSize/(height - 1)
    VRatio = (VCenter - y) * VPixel
    return distance * VRatio

def getHorizontalCoordinate(x, distance):
    # realsense RGB : FOV 60.4 x 42.5 x 77 (H V D)
    # realsense Depth : FOV 73 x 58 x 95 (H V D)
    HFov2 = math.radians(69.4 / 2)
    HSize = math.tan(HFov2) * 2
    Hcenter = (width -1 ) /2 
    HPixel = HSize/(width - 1)
    HRatio = (x - width) * HPixel
    return distance * HRatio   


# Bounding box in ROI
bbox =  (50, 50, 100, 100)

pipeline =rs.pipeline()
config =rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8,30)

pipeline.start(config)

try:
    while True:

        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        images = np.hstack((color_image, depth_colormap))
        cv2.circle(images,(300,200),5,(0,0,255),-1)
        print depth_frame.get_distance(300,300)
        cv2.namedWindow('RS', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)


finally :

    pipeline.stop()
