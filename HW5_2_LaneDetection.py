import numpy as np
import matplotlib
import imutils
import cv2

def snip_image(img):
    snip = img[(img.shape[0]-300):(img.shape[0]-50), (0):(img.shape[1])]
    return snip

def mask_image(img):
    mask = np.zeros((img.shape[0], img.shape[1]), dtype = "uint8")
    pts = np.array([[90, img.shape[0]-25], [90, img.shape[0]-35], [int(img.shape[1]/2)-30, 100],
                   [int(img.shape[1]/2)+30, 100], [img.shape[1]-90, img.shape[0]-35], [img.shape[1]-90, img.shape[0]-25]], dtype = np.int32)

    cv2.fillConvexPoly(mask, pts, 255)
    masked = cv2.bitwise_and(img, img, mask = mask)

    return masked

def thres_image(img):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Grayscale", gray)
    #thres = 60
    #thresholded = cv2.threshold(gray, thres, 255, cv2.THRESH_BINARY)[1]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #whiteLower = np.array([17, 40, 147])
    #whiteUpper = np.array([255, 76, 255])
    whiteLower = np.array([30, 0, 65]) #For Video 1
    whiteUpper = np.array([255, 255, 150]) #For Video 1
    #whiteLower = np.array([17, 40, 65]) # attempted average
    #whiteUpper = np.array([255, 76, 255]) # attempted average

    white_lane_mask = cv2.inRange(hsv, whiteLower, whiteUpper)
    #cv2.imshow("White Lane Lines", white_lane_mask)

    #yellowLower = np.array([12, 0, 161]) #161 Videos 2 and 30
    #yellowUpper = np.array([255, 255, 255]) # Videos 2 and 30
    #yellow_lane_mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    thresholded = cv2.bitwise_and(img, img, mask = white_lane_mask)
    #thresholded = cv2.bitwise_and(img, img, mask = yellow_lane_mask)
    return thresholded

def blur_Image(img):
    return cv2.GaussianBlur(img, (9, 9), 0)

def find_edges(img):
    return cv2.Canny(img, 30, 100)

def line_image(img):
    #lines = cv2.HoughLinesP(img, 1, np.pi/180, 30)
    lines = cv2.HoughLines(img, 1, np.pi/180, 30)
    return lines

x1s = None
x2s = None
x1s2 = None
x2s2 = None
def draw_hough_lines(image, lines):
    global x1s, x2s, x1s2, x2s2
    if lines is None:
        print("No lines detected.")
        return
      # Averaging Variables
    rhoLeft = 0
    rhoRight = 0
    thetaLeft = 0
    thetaRight = 0
    countLeft = 0
    countRight = 0
    # Iterate over detected lines
    for rho, theta in lines[:, 0]:
        if rho > 0:
            rhoLeft += rho
            thetaLeft += theta
            countLeft += 1
        else:
            rhoRight += rho
            thetaRight += theta
            countRight += 1
            
    # Compute the average rho and theta
    avgRhoLeft = rhoLeft / countLeft if countLeft > 0 else 0
    avgThetaLeft = thetaLeft / countLeft if countLeft > 0 else 0
    avgRhoRight = rhoRight / countRight if countRight > 0 else 0
    avgThetaRight = thetaRight / countRight if countRight > 0 else 0

# Draw the average line for Left Lane
    a = np.cos(avgThetaLeft)
    b = np.sin(avgThetaLeft)
    x0 = a * avgRhoLeft
    y0 = b * avgRhoLeft
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    if y2 < 100:
        if x2-x1 == 0:
            x1 = x1s
            x2 = x2s
        m = (y2-y1)/(x2-x1)
        y2 = 100
        x2 = int((y2-y1)/m + x1)
    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 5) # Draw average line in blue
    if x2-x1 != 0:
        x1s = x1
        x2s = x2

  # Draw the average line for Right Lane
    a = np.cos(avgThetaRight)
    b = np.sin(avgThetaRight)
    x0 = a * avgRhoRight
    y0 = b * avgRhoRight
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))   
    if y1 < 100:
        if int(x2-x1) == 0:
            x1 = x1s2
            x2 = x2s2
            print("hello")
        m = (y2-y1)/(x2-x1)
        y1 = 100
        x1 = int((y1-y2)/m + x2)        
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 5) # Draw right lane in red
    if x2-x1 != 0:
        x1s2 = x1
        x2s2 = x2

def main():
    video1 = cv2.VideoCapture('test_video_01.mp4')
    video2 = cv2.VideoCapture('test_video_02.mp4')
    video3 = cv2.VideoCapture('30.mp4')
    #image = cv2.imread("testimage.jpg")
    #image = cv2.imread("yellow_lane_lines-01.jpg")
    while video2.isOpened():
        ret, frame = video2.read()
        snip = snip_image(frame)
        mask = mask_image(snip)
        thresholded = thres_image(mask)
        blurred_image = blur_Image(thresholded)
        image_edges = find_edges(blurred_image)
        lines = line_image(image_edges)

        draw_hough_lines(snip, lines)
        #print(lines)

        cv2.imshow("Original Test Image", frame)
        #cv2.imshow("Snipped Image", snip)
        cv2.imshow("Mask", mask)
        cv2.imshow("Thresholded", thresholded)
        #cv2.imshow("Blurred Image", blurred_image)
        cv2.imshow("Image Edges", image_edges)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
