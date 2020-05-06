import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import multiprocessing as mp
from scenestich import get_features, match_features, ransac


# THIS IS THE ONE WE ARE USING THIS IS THE RIGHT ONE AH
def inverseCyl(img, f):
    height = img.shape[0]
    width = img.shape[1]

    cyl = np.zeros_like(img)
    cyl_mask = np.zeros_like(img)
    cyl_h, cyl_w, cly_d = cyl.shape
    x_c = float(cyl_w) / 2.0
    y_c = float(cyl_h) / 2.0
    for x_cyl in np.arange(0,cyl_w):
        for y_cyl in np.arange(0,cyl_h):
            theta = (x_cyl - x_c) / f
            h = (y_cyl - y_c) / f
            X = np.array([math.sin(theta), h, math.cos(theta)])
            x_im = (f * (X[0]/X[2])) + x_c
            if x_im < 0 or x_im >= width:
                continue
            y_im = (f * (X[1]/X[2])) + y_c

            if y_im < 0 or y_im >= height:
                continue

            cyl[int(y_cyl),int(x_cyl)] = img[int(y_im),int(x_im)]
            cyl_mask[int(y_cyl),int(x_cyl)] = 255

    return (cyl,cyl_mask)

def pano(warped):
    
    stitched_image = warped[0].copy()
    shift_list = [[0,0]]
    previous_features = [[], []]

    for i in range(1, len(warped)):
        img1 = warped[i-1]
        img2 = warped[i]

        kp1, des1 = previous_features
        if len(des1) == 0:
            kp1, des1 = get_features(img1)

        kp2, des2 = get_features(img2)
        previous_features = [kp2, des2]



        feature_matches = match_features(kp1, des1, kp2, des2, img1, img2)


        print("Features have been matched !")
        H = ransac(feature_matches, kp1, kp2)
        shift = [H[1][2], H[0][2]]
        print("Best shift has been found !")
        print(shift)

        shift_list += [shift]
        stitched_image = stitch(stitched_image, img2, shift)
        print("Images have been stitched !")
        # plt.imshow(stitched_image)
        # plt.show()
        # cv2.waitKey(0)

    return stitched_image


def blend(r2, r1, seam):
    new_row = np.zeros(shape=r1.shape, dtype=np.uint8)
    window = 2

    for x in range(len(r1)):
        color1 = r1[x]
        color2 = r2[x]
        if x < seam - window:
            new_row[x] = color2
        elif x > seam + window:
            new_row[x] = color1
        else:
            ratio = (x - seam + window)/( window * 2)
            new_row[x] = (1 - ratio)*color2 + ratio*color1

    return new_row

def stitch(img1, img2, shift):
    shift[0] = int(shift[0])
    shift[1] = int(shift[1])
    padding = [
        (int(shift[0]), 0) if shift[0] > 0 else (0, int(-shift[0])),
        (0,0),
        (0, 0)
    ]
    shifted_img1 = np.lib.pad(img1, padding, 'constant', constant_values=0)
    horiz = int(shifted_img1.shape[1]) - int(abs(shift[1]))
    vert = int(abs(shift[0]))

    shifted_img1 = shifted_img1[vert:, :horiz]
    # plt.imshow(shifted_img2)
    # plt.show()
    # cv2.waitKey(0)

    stitched = np.concatenate((shifted_img1, img2), axis=1)

    return stitched