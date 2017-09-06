##############################################################################
#########################  Fundus_Cam.py                              ########
#########################  Primary Author: Ebin                       ########
#########################  Version : 1.0                              ########
#########################  Contributor: Preetha Warrier, Ayush Yadav  ########
##############################################################################


from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np
import io
import ftplib
from ftplib import FTP
import os
# initilise FTP object
ftp  = FTP()



###############################################################################
### This class provides access to the picamera and its associated functions ###
###############################################################################

class Fundus_Cam(object):

    # The constructor initializes the camera object and starts preview
    def __init__(self, framerate=10,preview=False):

        # initialize the camera
        self.camera = PiCamera()
        self.camera.resolution = self.camera.MAX_RESOLUTION
        self.camera.framerate = framerate

        # stream is a file-like type used to store captured images to memory
        # rather than onto disk
        self.stream = io.BytesIO()

        # this determines the vertical flip_state of the picamera
        # this can be toggled by Fundus_Cam.flip_cam()
        self.flip_state=False

        # This is a list to store images captured
        # in Fundus_Cam.continuous_capture()
        self.images=[]
        #self.camera.start_preview()
        self.camera.start_preview(fullscreen = False,window = (100,100,640,480))

        # used to stop and start recording in versions higher than1.0
        self.stopped = False


    def start_prev(self):
    	self.camera.start_preview()
        self.stopped = False


    def continuous_capture(self):
        # starts a new thread, which runs the update()
        self.stopped = False
        Thread(target=self.update, args=()).start()


    # continuosly captures frames from the camera, in a seperate thread
    def update(self):
        # keep looping infinitely until the thread is stopped
        # In version 1.0 it grabs only 10 frames
        while True:
                # grab the frame from the stream
                self.camera.capture(self.stream,format='jpeg',use_video_port=True)
                # convert the frame captures to numpy array and append to images
                self.images.append(np.fromstring(self.stream.getvalue(),dtype=np.uint8))
                # clear the stream for the next frame
                self.stream.truncate()
                self.stream.seek(0)
                if(len(self.images)>9):
                    self.stopped=True
                    return


    # to flip the current state
    def flip_cam(self):
        self.camera.vflip=(not self.camera.vflip)

    #to capture a single image
    def capture(self):
        self.camera.capture(self.stream,format='jpeg',use_video_port=True)
        # convert to numpy array
        self.image=np.fromstring(self.stream.getvalue(),dtype=np.uint8)
        # clear the stream
        self.stream.truncate()
        self.stream.seek(0)
        # return the captured image
        return self.image

    # to start camera preview
    def preview(self):
        self.camera.start_preview(fullscreen=False,window = (100,100,640,480))

    # to stop camera preview
    def stop_preview(self):
        self.camera.stop_preview()

    # used in version higher than 1.0
    def stop(self):
        self.camera.close()
        self.stopped=True

    #get the corresponding ftp folder, if it does not exist create it
    def get_ftp_folder(self,source):
        try:
            ftp.cwd(source)
            print ftp.pwd()
        except ftplib.error_perm:
            ftp.mkd(source)
            ftp.cwd(source)
            print 'created a new folder', source

    # to copy files from the given location
    def copyfiles(self,source):
        #change working directory of local
        os.chdir(source)
        #change/create working directory of ftp server
        self.get_ftp_folder(source)
        for root, dirs, filenames in os.walk(source):
            for f in filenames:
                print 'Copying ',f
                #ftp.cwd()
                ftp.storbinary('STOR %s' % f,open(f,'rb'))
        return

    # to start copying files
    def copy_files(self,HOST,PORT,source):
        print 'HOST:',HOST
        print 'PORT:',PORT
        print 'source:',source
        # get connection to the specified HOST and PORT
        ftp.connect(HOST,PORT)
        print 'connected to ',HOST
        ftp.login()
        # copy files from the MR number folder
        self.copyfiles(source)

        return 'Copy complete.'


## decode function
## decode,process and save the grabbed image
## the decode function has been moved to the fundus_mod3.py file for easy access


##    def decode_image(images,path_sen,name):
##    #name=raw_input("enter the name to be saved")
##        no=1
##        if type(images) is list:
##
##            for img in images:
##                image=cv2.imdecode(img,1)
##                #image=get_fundus(image)
##                cv2.imwrite(path_sen + name + '_'+str(no)+'.jpg',image)
##                no=no+1
##        else:
##            image=cv2.imdecode(images,1)
##            #image=get_fundus(image)
##            cv2.imwrite(path_sen + name + '.jpg',image)


##############################################################################
#####################    End of Class Implementation  ########################
##############################################################################



# for debugging
if __name__=='__main__':

    fundus_cam=Fundus_Cam()
    ## this part of the code is for debugging and testing the Fundus_Cam class
    image=fundus_cam.capture()
    raw_input("start continuous??")
    fundus_cam.continuous_capture()
    while not fundus_cam.stopped:
        pass
    print "decoding still"
    decode_image(image)
    print "decoding continuous capture"
    decode_image(fundus_cam.images)
    fundus_cam.stop_preview()






