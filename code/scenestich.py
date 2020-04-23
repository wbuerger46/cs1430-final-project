import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def get_feature_points(images):
    sift = cv.Sift()


'''
This function takes in two images and uses SIFT and K-nearest-neighbors
matching to match keypoints between the two images
'''
def stitch_two_images(img1, img2):
    sift = cv.xfeatures2d.SIFT_create()
    img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    matcher = cv.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    best_matches = []
    for im1point, im2point in matches:
        if im1point.distance < 0.3 * im2point.distance:
            best_matches.append([im1point])

    img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, best_matches, None, flags=2)

    plt.imshow(img3)
    plt.show()

