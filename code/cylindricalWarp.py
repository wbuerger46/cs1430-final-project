import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
from scenestich import get_features, match_features, ransac

# Given an image and the cameras focal distance, project the image onto cylindrical coordinates
def inverseCyl(img, f):
    height = img.shape[0]
    width = img.shape[1]

    cyl = np.zeros_like(img)
    #cyl_mask = np.zeros_like(img)
    cyl_h, cyl_w, cly_d = cyl.shape
    x_c = float(cyl_w) / 2.0
    y_c = float(cyl_h) / 2.0
    # Loops through every pixel in the cyl image
    for x_cyl in np.arange(0,cyl_w):
        for y_cyl in np.arange(0,cyl_h):
            # Calculates cylindrical coordinates (sin(theta), h, cos(theta))
            theta = (x_cyl - x_c) / f
            h = (y_cyl - y_c) / f
            X = np.array([math.sin(theta), h, math.cos(theta)])
            # Calculates the warped X pixel location
            x_im = (f * (X[0]/X[2])) + x_c
            if x_im < 0 or x_im >= width:
                continue
            # Calculates the warped y pixel location
            y_im = (f * (X[1]/X[2])) + y_c

            if y_im < 0 or y_im >= height:
                continue
            # If both pixel values are in bounds, store it in the cylindrical location
            cyl[int(y_cyl),int(x_cyl)] = img[int(y_im),int(x_im)]
            #cyl_mask[int(y_cyl),int(x_cyl)] = 255

    return cyl

# Given a list of cylindrical images, stitches them into a 360 degree panorama
def pano(warped):
    
    #the leftmost image will start in stitched_image
    stitched_image = warped[0].copy()
    previous_features = [[], []]

    # Loops through every image in the list, stitching them together from left to right
    for i in range(1, len(warped)):
        img1 = warped[i-1]
        img2 = warped[i]

        # Gets the feature points for the two images
        kp1, des1 = previous_features
        if len(des1) == 0:
            kp1, des1 = get_features(img1)
        kp2, des2 = get_features(img2)
        previous_features = [kp2, des2]

        # Get the list of best matches from the two sets of feature points
        feature_matches = match_features(kp1, des1, kp2, des2)
        print("Features have been matched !")

        # Get the homography matrix  based on these feature matches
        H = ransac(feature_matches, kp1, kp2)
        # Based on the homography matrix of a shift translation, gets the x and y shift
        shift = [H[1][2], H[0][2]]
        print("Best shift has been found !")
        print(shift)

        # Based on the shift, stitch the images together
        stitched_image = stitch(stitched_image, img2, shift)

        print("Images have been stitched !")

    return stitched_image

#Given two images and the shift, stitch the images together
def stitch(img1, img2, shift):
    shift[0] = int(shift[0])
    shift[1] = int(shift[1])
    # Madds the left image to account for vertical shift
    padding = [
        (int(shift[0]), 0) if shift[0] > 0 else (0, int(-shift[0])),
        (0,0),
        (0, 0)
    ]
    shifted_img1 = np.lib.pad(img1, padding, 'constant', constant_values=0)
    # Gets the horizontal and verticle shift to splice the first image
    horiz = int(shifted_img1.shape[1]) - int(abs(shift[1]))
    vert = int(abs(shift[0]))
    shifted_img1 = shifted_img1[vert:, :horiz]
    # Concatenates the splices left image to the right image
    stitched = np.concatenate((shifted_img1, img2), axis=1)

    return stitched