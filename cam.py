import cv2
import numpy as np
from picamera2 import Picamera2
import argparse
import glob


# Read the original image
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

cap = cv2.VideoCapture(0) # Camera is 480 x 640

while True:
    frame = cv2.rotate(picam2.capture_array(), cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('Video',frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
quit()
