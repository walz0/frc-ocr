from inspect import currentframe
import cv2
import numpy as np
from matplotlib import pyplot as plt
import main

TEAM_NUM_RATIO = 0

def getQuads(src):
    # output array
    quads = []
    # converting image into grayscale image
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # setting threshold of gray image
    ret, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # using a findContours() function
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # here we are ignoring first counter because 
    # findcontour function detects whole image as shape
    contours = contours[1:]
    for contour in contours:
        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        M = cv2.moments(contour)
        # centroid
        x, y = None, None
        area = M['m00']
        if area != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        # if feature is a quad
        if len(approx) == 4 and (x != None and y != None):
            #cv2.drawContours(src, [contour], 0, (0, 0, 255), 5)
            quads += [cv2.boundingRect(contour)]
    cv2.imshow("test", src)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return quads

# returns True if source image is a potential match frame
def isMatchView(src):
    # get all quads in image
    quads = getQuads(src)
    #for q in quads:
    #    if q 
    pass

video = cv2.VideoCapture("frc2.mp4")
currentFrame = 0
while True:
    ret, frame = video.read()
    if ret:
        frame = frame[0:255, 400:1300]
        if currentFrame % 2 == 0:
            quads = getQuads(frame)
            for q in quads:
                x,y,w,h = q
                print(w/h)
        currentFrame += 1
    else:
        break
