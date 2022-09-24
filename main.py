# from PIL import image
import os
import cv2
import pytesseract
import numpy as np
import time
from PIL import Image

def getFrame(frame, path):
    video = cv2.VideoCapture(path) 
    currentFrame = 0
    while True:
        if currentFrame == frame:
            ret,frame = video.read()
            if ret:
                return frame
            else:
                break
        currentFrame += 1
    video.release() 
    cv2.destroyAllWindows()
    return None

def extractData(frame, pos):
    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_TOZERO); 
    th, frame = cv2.threshold(frame, 210, 255, cv2.THRESH_BINARY); 

    # Isolate data from the frame
    if pos == "top":
        frame = frame[0:255, 400:1300]
    elif pos == "bottom":
        frame = frame[1080-255:1080, 400:1300]

    match = pytesseract.image_to_string(frame[10:70, :450]).split("\n")[0].strip()

    teams = []
    for i in range(6):
        if i == 0:
            teams += [frame[127:157, 260:356]]
        elif i == 1:
            teams += [frame[165:193, 260:356]]
        elif i == 2:
            teams += [frame[202:230, 260:356]]
        elif i == 3:
            teams += [frame[127:157, 755:850]]
        elif i == 4:
            teams += [frame[165:193, 755:850]]
        elif i == 5:
            teams += [frame[201:230, 755:850]]

    red, blue = [], []
    for _ in range(len(teams)):
        padding = Image.new("RGB", (150,50), color="white")
        padding.paste(Image.fromarray(teams[_]), (15, 10))
        team = pytesseract.image_to_string(padding)
        if _ < 3:
            blue += [team.split("\n")[0].strip()]
        else:
            red += [team.split("\n")[0].strip()]

    return {
        "slug": match,
        "alliances": {
            "blue": blue,
            "red": red
        }
    }

if __name__ == "__main__":
    frame = getFrame(20, "./frc4.mp4")
    cv2.imwrite("test.png", frame)
    start = time.time()
    print(extractData(frame, "bottom"))
    end = time.time()
    print(end - start)
