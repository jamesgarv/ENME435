# ENME489Y: Remote Sensing

# import the necessary packages
from picamera2 import Picamera2
import numpy as np
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = Picamera2()
config = camera.configure(camera.create_preview_configuration(main={"size": (1440, 1080)}))
camera.start()

# allow the camera to setup
time.sleep(1)

# Enter distance from wall, entered by the user
d = input("Please enter distance from wall, in inches: ")
print("Confirming the distance you entered is: ", d)

# grab an image from the camera
while True:

	image = camera.capture_array()
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	image = cv2.flip(image,-1)

	# plot semi-crosshairs for alignment
	cv2.line(image, (720, 0), (720, 1080), (0, 150, 150), 1)
	cv2.line(image, (0, 540), (1440, 540), (0, 150, 150), 1)

	# display distance from the wall, for reference
	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	red = (0, 0, 255)
	cv2.putText(image, d, (1080, 200), font, 10, red, 10)

	# display the image on screen and wait for a keypress
	cv2.imshow("Image", image)
	key = cv2.waitKey(1) & 0xFF

	# proceed as specified by the user

	# press q to break out of video stream
	if key == ord("q"):
		break

	# press m to save .jpg image with distance as filename
	if key == ord("m"):
		d = int(d)
		filename = "%d.jpg" %d
		cv2.imwrite(filename, image)
		break

cv2.destroyAllWindows()
camera.stop()
