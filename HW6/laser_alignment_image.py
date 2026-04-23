# ENME489Y: Remote Sensing (Updated for picamera2)

from picamera2 import Picamera2
import numpy as np
import time
import cv2

# initialize the new PiCamera2
picam2 = Picamera2()
config = picam2.configure(picam2.create_preview_configuration(main={"size": (1440, 1080)}))
picam2.start()

# allow the camera to setup
time.sleep(1)

# main capture loop
while True:
    # grab an image from the camera
    image = picam2.capture_array()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # may need to flip image, depending on mechanical setup of instrument
    image = cv2.flip(image, -1)

    # plot crosshairs, for alignment
    cv2.line(image, (720, 0), (720, 1080), (0, 150, 150), 1)
    cv2.line(image, (0, 540), (1440, 540), (0, 150, 150), 1)

    # plot green vertical lines, for alignment
    for i in range(50, 1450, 50):
        cv2.line(image, (i, 0), (i, 1080), (0, 150, 0), 3)

    # display the image
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF

    # break out of video loop when specified by the user
    if key == ord("q"):
        break

# cleanup
cv2.destroyAllWindows()
picam2.stop()
