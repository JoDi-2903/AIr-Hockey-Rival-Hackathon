# import the necessary packages
from collections import deque
import numpy as np
import cv2
import imutils

# Kamera-Index (0 intern most of the time here 1)
camera_index = 1

# access to camera
cap = cv2.VideoCapture(camera_index)  # Optional: CAP_DSHOW für Windows Performance

# Resolution and focus
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 5)

# Check if Camera is accesible
if not cap.isOpened():
    print("Kamera konnte nicht geöffnet werden.")
    exit()

print("Drücke 'q' zum Beenden.")

# detect different reds with color, saturation and brightness, set point length
redLower1 = (0, 120, 70)
redUpper1 = (10, 255, 255)
redLower2 = (150, 120, 70)
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

    # loop over the contours
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        else:
            center = (0, 0)

        # calculate the radius and circularity
        perimeter = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        # only proceed if the radius meets a minimum size and circularity is above a threshold
        if area > 500 and circularity > 0.7:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #display detected center in log
            print(f"Puck detected at: {center}")

            # update the points queue
            pts.appendleft(center)

            # loop over the set of tracked points
            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen, frame regular view, mask object view
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# close all windows
cap.release()
cv2.destroyAllWindows()