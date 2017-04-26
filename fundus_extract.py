'''
--------------------------------------------------------------------------
		Extraction of the Fundus from the Image
--------------------------------------------------------------------------
		Author: Shivakshit Patri
		Synopsis: A very simple piece of code in openCV to identify & seperate the Fundus from the image.
		Built for OWL (part of openDR project at Srujana Center for Innovation, LV Prasad Eye Institute, Hyderabad, India)
'''
import cv2
import numpy as np

img = cv2.imread('File_001.jpeg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([0,50,50])
upper_yellow = np.array([60,255,255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
dil = mask
im, contours, hierarchy = cv2.findContours(dil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
maxContour = 0

for contour in contours:
    contourSize = cv2.contourArea(contour)
    if contourSize > maxContour:
        maxContour = contourSize
        maxContourData = contour
mask2 = np.zeros_like(mask)
cv2.fillPoly(mask2,[maxContourData],255)

#(x,y),radius = cv2.minEnclosingCircle(maxContourData)
#cv2.circle(mask2,(int(x),int(y)),int(radius),255,-1)
mask3 = np.zeros_like(mask)

ellipse = cv2.fitEllipse(maxContourData)
cv2.ellipse(mask3,ellipse,255,-1)


finalImage = np.zeros_like(img)
finalImage = cv2.bitwise_and(img,img,mask=mask3)
cv2.namedWindow('final', cv2.WINDOW_NORMAL)
cv2.imshow('final',finalImage)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
cv2.namedWindow('Image3', cv2.WINDOW_NORMAL)
cv2.namedWindow('Image4', cv2.WINDOW_NORMAL)

cv2.imshow('Image', mask)
cv2.imshow('Image2', dil)
cv2.imshow('Image3', mask3)
cv2.imshow('Image4', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
