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
        self.isv3 = imutils.is_cv3()
        self.cachedH = None

    def stitch(self, images, ratio = 0.75, reprojThesh = 4.0, showMatches = False):
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
