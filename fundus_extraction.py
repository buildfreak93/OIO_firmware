'''
----------------------------------------------------------------------------------------------------------------------------------
		                        Extraction of the Fundus from the Image
----------------------------------------------------------------------------------------------------------------------------------
		Author: Shivakshit Patri
		Synopsis: A very simple piece of code in openCV to identify & seperate the Fundus from the image.
		Built for OWL (part of openDR project at Srujana Center for Innovation, LV Prasad Eye Institute, Hyderabad, India)
'''

import cv2
import numpy as np

class image_proc:

    # This process retains the fundus and masks out the rest of the image.
    @staticmethod
    def fundus_mask(image):
        
        # Thresholding Based on Color (0,50,50)
        mask = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        mask[:,:,0] = mask[:,:,0] + 20
        mask = cv2.inRange(mask,np.array([0,50,50]),np.array([40,255,255]))

        # Finding the blobs in the image.
        im, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        maxContour = 0

        # Finding the largest of the blobs.
        for contour in contours:
            contourSize = cv2.contourArea(contour)
            if contourSize > maxContour:
                maxContour = contourSize
                maxContourData = contour

        # Fitting an ellipse around the blob.
        mask = np.zeros_like(mask)
        cv2.ellipse(mask,cv2.fitEllipse(maxContourData),255,-1)
        
        # Masking the image.    
        return cv2.bitwise_and(image,image,mask=mask)

    @staticmethod
    def log_transform(image): 
        return (np.log((image+0.01).astype('float'))*(255/np.log(256))).astype('uint8')

    @staticmethod
    def inv_log_transform(image):
        return (np.exp(image.astype('float')*(np.log(256)/255)) - 0.01).astype('uint8')
    
    @staticmethod
    def scale_image(img):
        img = img.astype('float')
        img2 = np.zeros_like(img)
        for i in range(0,3):
            minVal = img[:,:,i].min()
            maxVal = img[:,:,i].max()
            img2[:,:,i] = 255*((img[:,:,i]-minVal)/(maxVal-minVal))
        return img2
