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
  print(f"\nLooped {counter} times")

  # Force take two separate images
  print("Capturing image...")
  # os.system('raspistill -n -t 1000 -o test%d.jpg --width 1000 --height 720')
  
  print("Analyzing images...")
  img1 = cv2.imread("test0.jpg")
  img2 = cv2.imread("test1.jpg")

  if img1 is None or img2 is None:
    print("Camera failed to capture images, skipping...")
    continue
  
  masked1, gray1 = mask_image(img1)
  masked2, gray2 = mask_image(img2)

  threshold = 50
  detector_total = np.uint64(0)
  detector = np.zeros((gray2.shape[0], gray2.shape[1]), dtype="uint8")

  # pixel by pixel comparison
  detector = np.where(np.abs(gray2.astype(int) - gray1.astype(int)) > threshold, 255, 0).astype("uint8")

  # sum detector array
  detector_total = np.uint64(np.sum(detector))
  print("detector_total = ", detector_total)
  print()

  if detector_total > 30000:
    print("Smart Doorbell has detected motion")

    # define unique name for a new video
    timestr = time.strftime("doorbell-%Y%m%d-%H%M%S")

    # command2 = "raspivid -n -w 1000 -h 720 -t 15000 -o " + timestr + ".h264"
    # os.system(command2)

    print("Finished recording...converting to mp4")

    # command3 = f"ffmpeg -r 30 -i {timestr}.h264 -c:v copy {timestr}.mp4" # MP4Box was not available so using ffmpeg instead
    # os.system(command3)

    print("Finished converting file, available for viewing")

    # write masked images to file
    cv2.imwrite("gray1.jpg", gray1)
    cv2.imwrite("gray2.jpg", gray2)
    cv2.imwrite("masked1.jpg", masked1)
    cv2.imwrite("masked2.jpg", masked2)

    # Upload video file to the cloud
    # fullDirectory = '/home/pi/SmartDoorbell/' + timestr + '.mp4'
    # command4 = 'sudo /home/pi/dropbox_uploader.sh upload ' + fullDirectory + ' /'
    # os.system(command4)

    # send email to user with images
    password = 'raspberrypi'
    yag = yagmail.SMTP('jamesgarvpi@gmail.com', password)

    f_time = datetime.now().strftime('%a %d %b @ %H:%M')
    images = ['test0.jpg', 'test1.jpg', 'gray1.jpg', 'gray2.jpg', 'masked1.jpg', 'masked2.jpg']
    
    # Optional: Comment out the next line if you don't want to wait for the email timeout during your video
    yag.send(to = 'jgarvey5@terpmail.umd.edu', subject = 'Smart Doorbell recording from: ' + f_time, 
             contents = "Smart Doorbell images: " + f_time, attachments = images)
    print("Email Delivered")

  else:
    print("Nothing detected")

  time.sleep(1)
