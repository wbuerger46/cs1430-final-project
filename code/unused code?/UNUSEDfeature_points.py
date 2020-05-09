import cv2

def get_feature_points(images):
    sift = cv2.xfeatures2d.SIFT_create()

    feature_points = []
    feature_descriptors = []
    for img in images:
        points, descriptors = sift.detectAndCompute(img, None)
        feature_points.append(points)
        feature_descriptors.append(descriptors)
    return feature_points, feature_descriptors