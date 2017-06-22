import picamera
from time import sleep
import RPi.GPIO as GPIO
import os
from sys import exit
import io
import cv2
import numpy as np
from threading import Thread

class MyCamera:
    def __init__(self):
        try:
            # Initialization of camera
            cam = picamera.PiCamera()

            # Set camera resolution
            #cam.resolution = cam.MAX_RESOLUTION

            # Initialization of GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)

            # Create a tuple of pin numbers
            pinNumber = (8,10,12,16,18,22,24,26,32,36,38,40)

            # Getting the current directory.
            currentDir = os.getcwd()

            # Creating directory structure.
            currentSession = self.create_dirs(currentDir,'/Session_')

            # Start camera feed.
            self.camFeed(cam, currentSession, pinNumber)

        except KeyboardInterrupt:
            print "\nCtrl + C encountered. Leds Switched Off. Program Exited."
            exit(0)

    def camFeed(self,cam,currentSession,pinNumber):

        # Initiate Preview.
        cam.start_preview(fullscreen = False,window = (100,100,640,480))
        while True:

            # Input Hotkey.
            key = raw_input('Input HotKey:\n')

            if key == 'q':
                cam.stop_preview()
                break

            elif key == 'p':
                pin = pinNumber[input("Enter Pin Number:\n")]
                GPIO.cleanup()
                GPIO.setup(pin,GPIO.OUT)
                GPIO.output(pin,GPIO.HIGH)

            elif key == 'c':
                image = []
                stream = io.BytesIO()
                cam.capture(stream,format='jpeg',use_video_port = True)
                Thread(target=self.write,args=(stream,i,)).start()
                stream.truncate()
                stream.seek(0)

            elif key == 'w':
                lon = input('Number of Leds to be switch on')
                images = []
                stream = [io.BytesIO() for i in range(12)]
                #cam.capture_sequence(stream,format='jpeg',use_video_port = True)
                for i in range(0,4):
                    cam.capture(stream[i],format='jpeg',use_video_port = True)
                    Thread(target=self.write,args=(stream,i,)).start()
                    stream[i].truncate()
                    stream[i].seek(0)



    def write(self,stream,i):
        image = np.fromstring(stream[i].getvalue(),dtype=np.uint8)
        img = cv2.imdecode(image,1)
        cv2.imwrite('abc_{}.jpg'.format(i),img)


    def create_dirs(self,currentDir,extension):
        # Directory count.
        i = 0
        # Directory name.
        newDir = ''

        while True:

            # Generate directory name.
            newDir = currentDir + extension + str(i)

            # Search if directory exists, if not create one.
            if not os.path.exists(newDir):
                os.makedirs(newDir)
                break
            # Incrementing the directory count.
            i = i + 1

        return newDir

camera = MyCamera()

