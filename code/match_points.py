import cv2

def match_points(img1_des, img2_des):
    matcher = cv2.FlannBasedMatcher()
    matches = matcher.knnMatch(img1_des, img2_des, k=2)

    threshold = 0.8

    good_matches = []
    for m, n in matches:
        if m.distance < threshold * n.distance:
            good_matches.append(m)
    # for i, (one, two) in enumerate(matches):
    #     if one.distance < threshold*two.distance:
    #         good_matches.append((one.trainIdx, one.queryIdx))
