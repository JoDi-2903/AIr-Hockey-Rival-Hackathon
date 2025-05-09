import cv2 
import numpy as np 

# import the necessary packages
from collections import deque
import numpy as np
import cv2
import imutils

# Kamera-Index (0 intern most of the time here 1)
camera_index = 1

# access to camera
cap = cv2.VideoCapture(camera_index)  # Optional: CAP_DSHOW für Windows Performance

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


# keep looping
while True:
# grab the current frame
	ret, frame = cap.read()
	if not ret:
		print("Kein Frame erhalten.")
		break

# Read image. 
#frame = cv2.imread('../../Pic/CA.jpg', cv2.IMREAD_COLOR) 

	# Convert to grayscale. 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

	# Blur using 3 * 3 kernel. 
	gray_blurred = cv2.blur(gray, (3, 3)) 

	# Apply Hough transform on the blurred image. 
	detected_circles = cv2.HoughCircles(gray_blurred, 
					cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
				param2 = 30, minRadius = 1, maxRadius = 40) 



	# Draw circles that are detected. 
	if detected_circles is not None: 

		# Convert the circle parameters a, b and r to integers. 
		detected_circles = np.uint16(np.around(detected_circles)) 

		for pt in detected_circles[0, :]: 
			a, b, r = pt[0], pt[1], pt[2] 

			# Draw the circumference of the circle. 
			cv2.circle(frame, (a, b), r, (0, 255, 0), 2) 

			# Draw a small circle (of radius 1) to show the center. 
			cv2.circle(frame, (a, b), 1, (0, 0, 255), 3) 
			cv2.imshow("Detected Circle", frame) 
			cv2.waitKey(0) 
			
		# show the frame to our screen
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the 'q' key is pressed, stop the loop
			if key == ord("q"):
				break

		# close all windows
		cap.release()
		cv2.destroyAllWindows()