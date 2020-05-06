from skimage.color import rgb2gray
from skimage import img_as_float32
from skimage.transform import rescale
import glob, os
import numpy as np
import cv2
from cv2 import imread
from multiStitch import multiStitch, crop
from cylindricalWarp import inverseCyl, pano
from cameraCal import calibrateCam
from matplotlib import pyplot as plt
import natsort


'''
This function loads all images in the given directory.
'''
def load_data(image_directory_path):
    os.chdir(image_directory_path)
    scale_factor = 0.5
    image_files = []
    names = []
    files = glob.glob("*.jpg")
    files = (natsort.natsorted(files,reverse=False))
    print(files)
    for im_file in files:
        image = imread(im_file)
        image_files.append(image)
        names.append(im_file)
    return image_files, names


def main():
    
    # mtx, dist, rvecs, tvecs = calibrateCam()
    images, fileNames = load_data("../data/cyl")
    ###########################################################################
    # DID THIS ALREADY SAVED THOSE IMAGES
    # warped = []
    # for i in range(len(images)):
    #     print(i)
    #     returned, ret_m = inverseCyl(images[i], mtx[0][0])
    #     cv2.imwrite("../data/cyl"+fileNames[i]+"_cyl.png", returned)
    #     warped.append(returned)
    ###########################################################################
    stitched_image = pano(images)
    cv2.imwrite("../results/panorama.png", stitched_image)
    plt.imshow(stitched_image) 
    plt.show()  



if __name__ == "__main__":
    main()