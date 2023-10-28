import cv2
import numpy as np
from picamera2 import Picamera2
import argparse
import glob

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

# Read the original image
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

cap = cv2.VideoCapture(0) # Camera is 480 x 640

while True:
    frame = picam2.capture_array()
    #ret, frame = cap.read()
    #frame = cv2.resize(frame, (1280, 960), fx = 0, fy = 0) # Enlarges the video 
 
    #frame = frame.astype('uint8') #MAYBE

    blur = cv2.GaussianBlur(frame, (3,3), 0) 

    edges = auto_canny(blur) # Canny edge detection
    edgesB = cv2.GaussianBlur(edges, (3,3), 0) # Makes edge smoother
    edges = cv2.addWeighted(edges, 1, edgesB, 1, 0.9) # Makes a "glowing" edge
    edges = cv2.merge((edges,edges,edges,edges))
   

    merge = cv2.addWeighted(frame, 1, edges, 1, 0.0)
    cv2.imshow('Video',merge)
    

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
quit()
