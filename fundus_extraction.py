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
