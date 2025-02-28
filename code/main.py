from skimage.color import rgb2gray
from skimage import img_as_float32
from skimage.transform import rescale
import glob, os
import numpy as np
import cv2
from cv2 import imread
from cylindricalWarp import inverseCyl, pano
from cameraCal import calibrateCam
from matplotlib import pyplot as plt
from panorama_viewer import PanoramaViewer
import natsort

## RUN THE VISUALIZER BY ITSELF WITH 'python3 panorama_viewer.py'


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
    
    # Loads the cylindrical images in
    images, fileNames = load_data("../data/cyl")
    ###########################################################################
    # This code generates the cylindrical images
    # It only needed to be run once, and now the images are saved in data/cyl
    ###########################################################################
    # mtx, dist, rvecs, tvecs = calibrateCam()
    # warped = []
    # for i in range(len(images)):
    #     print(i)
    #     returned, ret_m = inverseCyl(images[i], mtx[0][0])
    #     cv2.imwrite("../data/cyl"+fileNames[i]+"_cyl.png", returned)
    #     warped.append(returned)
    ###########################################################################
    
    # Gets the actual panorama from the warped images
    stitched_image = pano(images)

    # Saves and displays the stitched panorama
    cv2.imwrite("../results/panorama.png", stitched_image)
    PanoramaViewer("../results/panorama.png")



if __name__ == "__main__":
    main()