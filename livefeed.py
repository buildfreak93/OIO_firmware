import numpy as np
import cv2
import os
import time

# Creating the directory structure.
i = 0
currentpath = ''
newpath = ''
newfile = ''

while(True):
    currentpath = os.getcwd()
    newpath = currentpath+'/Session_'+str(i)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        capturepath = newpath + '/capture'
        os.makedirs(capturepath)
        burstpath = newpath + '/burst'
        os.makedirs(burstpath)
        break
    i = i + 1

# Starting the VideoCapture.
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Display the resulting frame
    cv2.namedWindow('myImage')
    cv2.imshow('myImage',frame)
    
    # Reading the keyboard input.
    key = cv2.waitKey(1) & 0xFF
    
    # Saving the image.
    if key == ord('c'):
        pin = input('Please specify pin number: ')
        commandline = 'python ledcontrol.py {}'.format(pin)
        os.system(commandline)
        i = 0
        while(True):
            newfile = capturepath + '/image_' + str(i) + '.jpg'
            if not os.path.isfile(newfile):
                cap.release()
                commandline = 'fswebcam -r 2592x1944 --no-banner {}'.format(newfile)
                os.system(commandline)
                cap = cv2.VideoCapture(0)
                break
            i = i + 1

    # Image burst
    if key == ord('b'):
        i = 0
        while(True):
            burstsession = burstpath+'/burst_'+str(i)
            if not os.path.exists(burstsession):
                os.makedirs(burstsession)
                break
            i = i + 1
        for pin in range(1,8):
            commandline = 'python ledcontrol.py {}'.format(pin)
            os.system(commandline)
            time.sleep(3)
            burst_image = '{}/burst_{}.jpg'.format(burstsession,pin)
            cap.release()
            commandline = 'fswebcam -r 2592x1944 --no-banner {}'.format(burst_image)
            os.system(commandline)
            cap = cv2.VideoCapture(0)
        commandline = 'python ledcontrol.py 0'
        os.system(commandline)

    # Quitting the gui
    if key == ord('q'):
        print 'quit'
        cv2.destroyWindow('frame')
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
