import picamera
from time import sleep
import RPi.GPIO as GPIO
import os
from cv2 import waitKey

class MyCamera():

    def __init__(self):
        # Initialize camera & adjust camera settings.
        cam, newPath = self.initCam()

        # Get camera feed & take images.
        self.camFeed(cam, newPath)

    def initCam(self):
        # Initialize Camera
        cam = picamera.PiCamera()

        # Set camera resolution to maximum
        cam.resolution = cam.MAX_RESOLUTION

        # Set camera framerate.
        cam.framerate = 12

        # Locking & setting exposure
        cam.exposure_mode = 'auto'
        #cam.exposure_compensation = 21

        # Initiating GPIO
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Creating Directory Structure
        i = 0
        currentPath = ''
        newPath = ''
        while True:
            currentPath = os.getcwd()
            newPath = currentPath+'/Session_'+str(i)
            if not os.path.exists(newPath):
                os.makedirs(newPath)
                capturePath = newPath + '/Capture'
                burstPath = newPath + '/Burst'
                os.makedirs(capturePath)
                os.makedirs(burstPath)
                break
            i = i + 1
        return cam, newPath

    def camFeed(self,cam, newPath):

        # Start camera feed
        while True:
            cam.start_preview(fullscreen=False, window = (100,100,640,480))
            GPIO.setup(11,GPIO.OUT)
            GPIO.setup(13,GPIO.OUT)
            GPIO.output(11,1)
            GPIO.output(13,1)
            key = raw_input("Enter the Hot Key:\n")

            # Hot key for quitting the video feed.
            if key == 'q':
                cam.stop_preview()
                break

            # Hot key for taking a picture.
            elif key == 'c':
                #led = input("Led Number:\n")
                #GPIO.setwarnings(False)
                #key1 = (led & 0b0001) != 0
                #key2 = (led & 0b0010) != 0
                #key3 = (led & 0b0100) != 0
                #GPIO.setup(11,GPIO.OUT)
                #GPIO.setup(13,GPIO.OUT)
                #GPIO.setup(15,GPIO.OUT)
                #GPIO.output(11,key1)
                #GPIO.output(13,key2)
                #GPIO.output(15,key3)
                i = 0
                while True:
                    newFile = newPath + '/Capture' + '/Image_' + str(i) + '.jpg'
                    if not os.path.isfile(newFile):
                        cam.capture(newFile)
                        break
                    i = i + 1

            # Hot key for burst mode.

            elif key == 't':
                GPIO.setup(11,GPIO.OUT)
                GPIO.setup(13,GPIO.OUT)
                GPIO.output(13,0)
                GPIO.output(11,1)
                i = 0
                while True:
                    newFile = newPath + '/Capture' + '/Image_' + str(i) + '.jpg'
                    if not os.path.isfile(newFile):
                        cam.capture(newFile)
                        break
                    i = i + 1
                i=i+1
                GPIO.output(11,0)
                GPIO.output(13,1)
                newFile = newPath + '/Capture' + '/Image_' + str(i) + '.jpg'
                cam.capture(newFile)
                GPIO.output(13,0)
                i=i+1
                GPIO.output(11,1)
                GPIO.output(13,1)
                newFile = newPath + '/Capture' + 'Image_' + str(i) + '.jpg'
                cam.capture(newFile)
                GPIO.output(11,0)
                GPIO.output(13,0)
            elif key == 'b':
                T = input("Time Interval:\n")
                led = 0
                while True:
                    sleep(T)
                    led = led + 1
                    key1 = (led & 0b0001) != 0
                    key2 = (led & 0b0010) != 0
                    key3 = (led & 0b0100) != 0
                    GPIO.setup(11,GPIO.OUT)
                    GPIO.setup(13,GPIO.OUT)
                    GPIO.setup(15,GPIO.OUT)
                    GPIO.output(11,key1)
                    GPIO.output(13,key2)
                    GPIO.output(15,key3)
                    key = cv2.waitKey() & 0xFF
                    if key == ord('c'):
                        cam.capture(newPath+'/Capture' + '/Image_' + str(i) + '.jpg')


camera = MyCamera()
