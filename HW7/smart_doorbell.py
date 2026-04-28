import numpy as np
import cv2
import time
import os
import yagmail
from datetime import datetime

def mask_image(img):
  mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")

  # masking area
  pts = np.array([[10, 10], [100, 10], [100, 100], [10, 100]], dtype=np.int32)
  
  cv2.fillConvexPoly(mask, pts, 255)
  masked = cv2.bitwise_and(img, img, mask=mask)
  gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (13, 13), 0)
  return masked, gray

counter = 0

while True:
  counter += 1
  print()
  print("Looped ", counter, " times")
  print()

  command = 'libcamera-still --width 1000 --height 720 -t 2100 --timelapse 1000 --nopreview -o test%d.jpg'
  os.system(command + " > /dev/null 2>&1") #removes print statement everytime a picture is taken

  print("Captured 1st & 2nd image for analysing")

  # Mask images
  test1 = cv2.imread("test1.jpg")
  test2 = cv2.imread("test2.jpg")

  threshold = 50
  detector_total = np.uint64(0)
  detector = np.zeros((gray2.shape[0], gray2.shape[1]), dtype="uint8")

  # pixel by pixel comparison
  for i in range(0, gray2.shape[0]):
    for j in range(0, gray2.shape[1]):
      if abs(int(gray2[i, j]) - int(gray1[i, jj])) > threshold:
        detector[i, j] = 255

  # sum detector array
  detector_total = np.uint64(np.sum)detector))
  print("detector_total = " detector_total)
  print()

  if detector_total > 30000:
    print("Smart Doorbell has detected motion")

    # define unique name for a new video
    timestr = time.strftime("doorbell-%Y%m%d-%H%M%S")
