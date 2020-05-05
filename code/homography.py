import cv2
import numpy as np

def find_homography(good_matches, img1_points, img2_points, img1, img2):
    source = np.float32([img1_points[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dest = np.float32([img2_points[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(source, dest, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([[0,0], [0,h-1], [w-1,h-1], [w-1,0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)