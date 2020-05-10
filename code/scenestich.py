import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import scipy.misc

# Creates CV2 Sift()
def get_feature_points(images):
    sift = cv.Sift()

# Uses SIFT to find and return all of the features in a given image
def get_features(image):
    sift = cv.xfeatures2d.SIFT_create()
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(img, None)
    # returns the keypoints and the feature discriptors for the given image
    return kp, des

# Given key points and feature discriptors for  2 images, return a list of the best feature matches between the images
def match_features(kp1, des1, kp2, des2):
    # Generates a list of feature matches
    matcher = cv.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    # Adds the matches that are within threshold to a list of best matches
    best_matches = []
    for im1point, im2point in matches:
        if im1point.distance < 0.2 * im2point.distance:
            best_matches.append([im1point])

    return best_matches

# Given a list of feature matches and key points from 2 images, calculates homography matrix
def ransac(matches, kp1, kp2):
    # Gets the actual points from the two images
    img1_points = np.float32([ kp1[m[0].queryIdx].pt for m in matches ]).reshape(-1,1,2)
    img2_points = np.float32([ kp2[m[0].trainIdx].pt for m in matches ]).reshape(-1,1,2)

    # Uses CV2's findHomography() to generate the homography matrix, H
    H, mask = cv.findHomography(img1_points, img2_points, cv.RANSAC, 5.0)

    return H