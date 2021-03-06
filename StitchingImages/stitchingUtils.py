'''
This file takes two images and stitches them together.

Written by Chris Walstra
Based heavily on code by Adrian Rosebrock (PyImageSearch)
'''

import imutils
import cv2
import numpy as np

class Stitcher:
    def __init__(self):
        self.cachedH = None

    # This function stitches two images together
    def stitch(self, images, ratio = 0.75, reprojThresh = 4.0, showMatches = False):
        (imageB, imageA) = images
        
        if self.cachedH is None:
            (kpsA, featuresA) = self.detectAndDescribe(imageA)
            (kpsB, featuresB) = self.detectAndDescribe(imageB)

            M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)

            if M is None:
                return None

            self.cachedH = M[1]

        result = cv2.warpPerspective(imageA, self.cachedH, 
                (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        return result

    # This function finds the points where it needs to stitch the images
    def detectAndDescribe(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        descriptor = cv2.xfeatures2d.SIFT_create()

        (kps, features) = descriptor.detectAndCompute(image, None)

        kps = np.float64([kp.pt for kp in kps])

        return (kps, features)

    # this function matches the points found above to actually stitch them
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []

        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance + ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        
        if len(matches) > 4:
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
            return (matches, H, status)

        return None
