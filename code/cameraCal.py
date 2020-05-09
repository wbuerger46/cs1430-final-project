import cv2
import numpy as np
import os
import glob
################################################################
# Calibrating our IPhone camera by following this OpenCV Guide:
# https://www.learnopencv.com/camera-calibration-using-opencv/
################################################################
def calibrateCam():
    # Defining the dimensions of our checkerboard as well as our criteria
    CHECKERBOARD = (7,9)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating arrays to store vectors of 3D points and 2D points (respectively) for each image
    objpoints = []
    imgpoints = [] 


    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    # Extracting and looping through each image of the checkerboard
    images = glob.glob('../data/checker/*.jpg')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        
        # If desired number of corners are found in the image then ret = true
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            imgpoints.append(corners2)

    # Perform camera Calibration using the 3D and 2D point corispondances we found
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # return the results of the calibration— we will be using mtx in the rest of our program
    return mtx, dist, rvecs, tvecs
