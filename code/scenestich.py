import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import scipy.misc

def get_feature_points(images):
    sift = cv.Sift()



def get_features(image):
    sift = cv.xfeatures2d.SIFT_create()
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(img, None)
    return kp, des

def match_features(kp1, des1, kp2, des2, img1, img2):
    matcher = cv.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    best_matches = []
    for im1point, im2point in matches:

        if im1point.distance < 0.2 * im2point.distance:
            best_matches.append([im1point])

    # # # Commented out for now
    # plt.imshow(img3) 
    # plt.show()   
    # cv.waitKey(0)
    return best_matches


def ransac(matches, kp1, kp2):
    img1_points = np.float32([ kp1[m[0].queryIdx].pt for m in matches ]).reshape(-1,1,2)
    img2_points = np.float32([ kp2[m[0].trainIdx].pt for m in matches ]).reshape(-1,1,2)

    H, mask = cv.findHomography(img1_points, img2_points, cv.RANSAC, 5.0)

    return H