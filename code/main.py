from skimage.color import rgb2gray
from skimage import img_as_float32
from skimage.transform import rescale
import glob, os
import numpy as np
from scenestich import stitch_two_images
from cv2 import imread
from multiStitch import multiStitch

'''
This function loads all images in the given directory.
'''
def load_data(image_directory_path):
    os.chdir(image_directory_path)
    scale_factor = 0.5
    image_files = []
    for im_file in glob.glob("*.jpg"):
        #mage = rgb2gray(img_as_float32(io.imread(im_file)))
        #image = np.float32(rescale(image, scale_factor))
        image = imread(im_file)
        image_files.append(image)
    return image_files


def main():
    images = load_data("../data")
    multiStitch(images)

    #stitch_two_images(images[0], images[1])
    #stitch_two_images(images[2], images[3])
    
    


if __name__ == "__main__":
    main()