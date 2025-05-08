# import the necessary packages
from collections import deque
import numpy as np
import cv2
import imutils

# Kamera-Index (0 intern most of the time here 1)
camera_index = 2

# access to camera
cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)  # Optional: CAP_DSHOW für Windows Performance

# Resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 5)

# Überprüfe, ob die Kamera geöffnet wurde
if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
    exit()

print("Drücke 'q' zum Beenden.")

# define the lower and upper boundaries of the "red puck
redLower1 = (0, 120, 70)
redUpper1 = (10, 255, 255)
redLower2 = (20, 120, 70)
redUpper2 = (180, 255, 255)
pts = deque(maxlen=64)

# keep looping
while True:
    # grab the current frame
    ret, frame = cap.read()
    if not ret:
        print("Kein Frame erhalten.")
        break

    # resize the frame, blur it, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "red"
    mask1 = cv2.inRange(hsv, redLower1, redUpper1)
    mask2 = cv2.inRange(hsv, redLower2, redUpper2)
    mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        # check if the contour is roughly circular
        perimeter = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        # only proceed if the radius meets a minimum size and circularity is above a threshold
        if radius > 3 and circularity > 0.3:
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# close all windows
cap.release()
cv2.destroyAllWindows()