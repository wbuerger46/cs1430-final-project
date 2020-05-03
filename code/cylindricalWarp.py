import cv2
import numpy as np

def cylindricalWarp(img, K):
    """This function returns the cylindrical warp for a given image and intrinsics matrix K"""
    height, width = img.shape[:2]
    # pixel coordinates
    y, x = np.indices((height,width))
    X = np.stack([x,y,np.ones_like(x)],axis=-1).reshape(height*width,3)
    K_inv = np.linalg.inv(K) 
    X = K_inv.dot(X.T).T # normalized coords
    # calculate cylindrical coords (sin\theta, h, cos\theta)
    A = np.stack([np.sin(X[:,0]),X[:,1],np.cos(X[:,0])],axis=-1).reshape(width*height,3)
    B = K.dot(A.T).T # project back to image-pixels plane
    # back from homog coords
    B = B[:,:-1] / B[:,[-1]]
    # make sure warp coords only within image bounds
    B[(B[:,0] < 0) | (B[:,0] >= width) | (B[:,1] < 0) | (B[:,1] >= height)] = -1
    B = B.reshape(height,width,-1)
    
    rgba = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA) # for transparent borders...
    # warp the image according to cylindrical coords
    return cv2.remap(rgba, B[:,:,0].astype(np.float32), B[:,:,1].astype(np.float32), cv2.INTER_AREA, borderMode=cv2.BORDER_TRANSPARENT)

def inverseCyl(img, f):
    Y = img.shape[0]
    X = img.shape[1]

    row = np.arange(X)

    xc = np.repeat(row, Y, axis=0)

    X_prime = np.zeros((Y,X))
    Y_prime = np.zeros((Y,X))

    X_prime = (f * np.tan((X - xc) / f)) + xc




