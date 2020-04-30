import numpy as np
import cv2
from matplotlib import pyplot as plt
import scipy.misc
import imutils


def multiStitch(images):
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    if status == 0:
        stitched = crop(stitched)
        cv2.imwrite("../results/zachbed_result.jpg", stitched)
        #cv2.imshow("Stitched", stitched)
        #cv2.waitKey(0)
        print("DONE  BITCH")
    else:
        print("bad things happened")
        print(status)



def crop(stitched):
    # stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
	# cv2.BORDER_CONSTANT, (0, 0, 0))
    gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    thresh = np.array(thresh)
    print(thresh.shape)
    shape1 = thresh.shape[0]
    shape0 = thresh.shape[1]
    left = []
    right = []
    top = []
    bottom = []
    for i in range(0, shape1):
        for j in range(0, shape0):
            if thresh[i,j] == 0:
                if i <= j and i <= shape0 - j and i <= shape1 - i:
                    if thresh[0:i,j][thresh[0:i,j] != 0].shape != (0,0):
                        top.append(i)
                elif j <= shape0 - j and j <= shape1 - i:
                    if thresh[i,0:j][thresh[i,0:j] != 0].shape != (0,0):
                        left.append(j)
                elif shape0 - j <= shape1 - i:
                    if thresh[i,j:shape0][thresh[i, j:shape0] != 0].shape != (0,0):
                        right.append(j)
                else:
                    if thresh[i:shape1,j][thresh[i:shape1,j] != 0].shape != (0,0):
                        bottom.append(i)
    l = max(left)
    r = min(right)
    t = max(top)
    b = min(bottom)
    stitched = stitched[t:b,l:r]
    #cv2.imwrite("../results/thresh.jpg", thresh)
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # c = max(cnts, key=cv2.contourArea)
    # mask = np.zeros(thresh.shape, dtype="uint8")
    # (x, y, w, h) = cv2.boundingRect(c)
    # cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
    # minRect = mask.copy()
    # sub = mask.copy()
    # while cv2.countNonZero(sub) > 0:
    #     minRect = cv2.erode(minRect, None)
    #     sub = cv2.subtract(minRect, thresh)
    # cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # c = max(cnts, key=cv2.contourArea)
    # (x, y, w, h) = cv2.boundingRect(c)
    # stitched = stitched[y:y + h, x:x + w]
    return stitched
