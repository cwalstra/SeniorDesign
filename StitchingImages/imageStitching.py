'''
This file stitches two images together using OpenCV's stitching library

Written by Chris Walstra based on work done by Adrian Rosebrock (PyImageSearch)
'''
from __future__ import print_function
from stitchingUtils import Stitcher
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

'''
TODO: Choose left/right
'''

def main():
    rightStream = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    stitcher = Stitcher()

    while True:
        right = leftStream.read()
        left = cv2.imread("leftSide.jpeg")

        left = imutils.resize(left, width=400)
        right = imutils.resize(right, width=400)

        result = stitcher.stitch([left, right], ratio = 100)

        if result is None:
            print("Homography could not be computed")
            break

        cv2.imshow("Left Frame", left)
        cv2.imshow("Right Frame", right)
        cv2.imshow("Result", result)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    print("Stopping")
    cv2.destroyAllWindows()
    rightStream.stop()



if __name__ == "__main__":
    main()
