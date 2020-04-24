import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import scipy.misc

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

    H = ransac(best_matches, kp1, kp2)

    height = img1.shape[0] + img2.shape[0]
    width = img1.shape[1] + img2.shape[1]

    result = cv.warpPerspective(img1, H, (width, height))
    result[0:img2.shape[0], 0:img2.shape[1]] = img2

    result = np.array(result)

    plt.figure(figsize=(20,10))
    plt.imshow(result)
    scipy.misc.toimage(result, cmin=0.0, cmax=...).save('bed_pic.jpg')

    plt.axis('off')
    plt.show()  


def ransac(matches, kp1, kp2):
    img1_points = np.float32([ kp1[m[0].queryIdx].pt for m in matches ]).reshape(-1,1,2)
    img2_points = np.float32([ kp2[m[0].trainIdx].pt for m in matches ]).reshape(-1,1,2)

    H, mask = cv.findHomography(img1_points, img2_points, cv.RANSAC, 5.0)

    return H
