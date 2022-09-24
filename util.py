import cv2

# macro for cv2 imshow and waitkey(0)
def imshow(src, title="frame"):
    cv2.imshow(title, src)
    cv2.waitKey(0)