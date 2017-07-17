#import matplotlib as plt
import numpy as np
import cv2
import os
from copy import deepcopy

def stitch(f1,f2,f3):

    print 'entered stitch'

    # Read the images to be aligned
    im1_aligned = cv2.imread(f1)
    im2 = cv2.imread(f2)
    im3 = cv2.imread(f3)
    final = cv2.imread(f1)
    print 'read files'

    #Covering Glare points in reference image
    im1 = deepcopy(im1_aligned)
    im1[850:1100,1350:1550]=0
    print 'masked glares in one image'

    # Convert images to grayscale
    im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    im3_gray = cv2.cvtColor(im3,cv2.COLOR_BGR2GRAY)
    print 'converted to gray scale'

    # Find size of image1
    sz = im1.shape
    print 'shape of image1'

    # Define the motion model
    warp_mode = cv2.MOTION_HOMOGRAPHY   		 
    print 'wrap mode set'

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
	warp_matrix = np.eye(3, 3, dtype=np.float32)
    else:
	warp_matrix = np.eye(2, 3, dtype=np.float32)
    print 'wrap matrix defined' 

    # Specify the number of iterations.
    number_of_iterations = 100
 
    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10
 
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
    print 'criteria set'

    # Run the ECC algorithm. The results are stored in warp_matrix.
    (cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
    (cc, warp_matrix) = cv2.findTransformECC (im1_gray,im3_gray,warp_matrix, warp_mode, criteria)
    print 'ECC started'

    if warp_mode == cv2.MOTION_HOMOGRAPHY :
	# Use warpPerspective for Homography
	im2_aligned = cv2.warpPerspective (im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else:
	# Use warpAffine for Translation, Euclidean and Affine
	im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);


    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        # Use warpPerspective for Homography
	im3_aligned = cv2.warpPerspective (im3, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else:
	# Use warpAffine for Translation, Euclidean and Affine
	im3_aligned = cv2.warpAffine(im3, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
    print 'completed alignment'

    for i in range (0,1944):
        for j in range (0,2592):
            final[i,j,0] = min(max(im1_aligned[i,j,0],im2_aligned[i,j,0]),max(im2_aligned[i,j,0],im3_aligned[i,j,0]),max(im3_aligned[i,j,0],im1_aligned[i,j,0]))
            final[i,j,1] = min(max(im1_aligned[i,j,1],im2_aligned[i,j,1]),max(im2_aligned[i,j,1],im3_aligned[i,j,1]),max(im3_aligned[i,j,1],im1_aligned[i,j,1]))
            final[i,j,2] = min(max(im1_aligned[i,j,2],im2_aligned[i,j,2]),max(im2_aligned[i,j,2],im3_aligned[i,j,2]),max(im3_aligned[i,j,2],im1_aligned[i,j,2]))
    print 'completed stitching'

    return final
