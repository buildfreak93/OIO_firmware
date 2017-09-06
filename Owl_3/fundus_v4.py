
##############################################################################
##  OWL v2.9                                                    ##############
## ------------------------------------------------------------ ##############
##  Authors: Preetha Warrier, Ayush Yadav, Devesh Jain,         ##############
##  Ebin Philip, Dhruv Joshi                                    ##############
##  Srujana Center for Innovation, LV Prasad Eye Institute      ##############
##                                                              ##############
##  This code will wait for an external button press, capture   ##############
##  two images in rapid succession with two different white     ##############
##  LEDs, process them to remove glare computationally, send    ##############
##  them to the theia algo backend to be processed, save them   ##############
##  and return the score on-screen in human readable format.    ##############
##                                                              ##############
##                                                              ##############
##  New in 2.6 :  Path corrected and Onscreen keyboard added    ##############
##  New in 2.9 :  Cleaned up code to conform to PEP-8 guidelines##############
##############################################################################

import pygame
import random
import csv
import subprocess
import argparse
import datetime
import time
import picamera
#import pigpio
import RPi.GPIO as GPIO
import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, session, g, url_for, flash
from flask import Response
from Fundus_Cam import Fundus_Cam
import cv2
import numpy as np
import wifi
from wifi import Cell, Scheme
import traceback
import requests
from requests.exceptions import RequestException
from requests.exceptions import ConnectionError
from pythonwifi.iwlibs import Wireless
from threading import Thread
from time import gmtime,strftime

from multiprocessing import Process, Queue, Event
from PIL import Image
from pygame.locals import *


# Import the modules needed for image processing and ML grading
import sys
#from sys import *
sys.path.insert(0, '/home/pi/openDR/modules/')

# adding modules folder to the start of python search path
import process      # our processing module
from process import grade
import extract
from extract import extract_fundus
import stitch
from stitch import stitch
# since the folder locations are fixed, hard-coding filesystem locations
base_folder = '/home/pi/OWL/'
#source = base_folder+'/images/'

#a dynamic grading key
grade_val = 'Grade'
gd = '-1'

switch = 4
i=1 # initial_counter
flag =1
enable = 0
wifi_check=0
no=0
text = ''
var_flip= 0
#file=open('mr.txt')
#text=file.readline()
#file.close()


wifi_name=''
wifi_password =''
networksfound=0
wifis=[]
led = []
led.append(8)
led.append(10)
led.append(12)
led.append(16)
led.append(18)
led.append(22)
led.append(24)
led.append(26)
led.append(32)
led.append(36)
led.append(38)
led.append(40)

alloff = [led[0],led[1],led[2],led[3],led[4],led[5],led[6],led[7],led[8],led[9],led[10],led[11]]
defaultOn = [led[0],led[4],led[8]]
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(alloff,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(defaultOn,GPIO.OUT, initial=GPIO.LOW)

last_img =  '1'

fontSize = 20
text_width=300
text_height=200

width=100
height=50

pos1_x=0
pos2_x=700
pos_y=400

msg_1="connect"
msg_2="Next"

fontStyle="Helvetica"
#to communicate between processes
global event1
global event2
global event3
global event4
global event5

event1 = Event()
event2 = Event()
event3 = Event()
event4 = Event()
event5 = Event()

display_width = 800
display_height = 480

black = (255,255,255)
white= (255,255,255)

blanchedalmond=(180,180,180)
chocolate=(0,0,0)
khaki=(240,230,140)
#olive=(128,128,0)
olive=(96,96,96)

#Initialization
pygame.init()
pygame.display.init()
#pygame.font()
#screen = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN,32)
screen = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
screen.fill(black)
#screen1 = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN,32)
screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
screen1.fill(black)

logo=pygame.image.load('/home/pi/openDR/owlLogo.jpg')
logo_resized=pygame.transform.scale(logo,(200,100))
logo_rot=pygame.transform.rotate(logo_resized,180)

#screen.blit(logo_resized,(300,30))
pygame.display.set_caption('OWL')
clock = pygame.time.Clock()
####

font = pygame.font.SysFont(fontStyle, 20)
text_flip = font.render('Flip', 0,(0,0,0))
text_strt = font.render('Start', 0,(0,0,0))
text_back = font.render('Back', 0,(0,0,0))
text_grd = font.render('Grade', 0,(0,0,0))
text_cap = font.render('Capture', 0,(0,0,0))
text_vid = font.render('Stitch', 0,(0,0,0))
text_copy = font.render('Copy', 0,(0,0,0))
text_warning = font.render('Please connect to wifi', 0,(0,0,0))

flip_rot=pygame.transform.rotate(text_flip,180)
start_rot=pygame.transform.rotate(text_strt,180)
back_rot=pygame.transform.rotate(text_back,180)
grade_rot=pygame.transform.rotate(text_grd,180)
video_rot=pygame.transform.rotate(text_vid,180)
cap_rot=pygame.transform.rotate(text_cap,180)
copy_rot=pygame.transform.rotate(text_copy,180)
###

x_cord = 100
y_cord = 10
width = 56
height = 20
text_x_cord = 20
text_y_cord = 60
count = 0
logo=pygame.image.load('/home/pi/openDR/owlLogo.jpg')
logo_resized=pygame.transform.scale(logo,(200,100))
screen.blit(logo_resized,(300,30))
#declaring object Fundus_cam
global obj_fc
obj_fc = Fundus_Cam()
#obj_fc.start_prev()
#obj_fc.stop()
wifiConnec = pygame.image.load('/home/pi/openDR/wifi.png')
wifiDisConnec=pygame.image.load('/home/pi/openDR/wifi_disabled.png')

wifiConnec_rot=pygame.transform.rotate(wifiConnec,180)
wifiDisConnec_rot=pygame.transform.rotate(wifiDisConnec,180)
try:
    def createFolder():
        print 'entered'
	global processed_text
        global base_folder
	print 'entered make a dir'
        d = base_folder + processed_text
        print d
        if not os.path.exists(d):
            print os.path.dirname(__file__)
            os.makedirs(d,0755)

    file=open('/home/pi/openDR/mr.txt')
    text=file.readline()
    file.close()

    date_var = datetime.datetime.now()
    processed_text = str(date_var.year)+'-'+str(date_var.month)+'-'+str(date_var.day)+'/'+text.upper() + '/images/'
    source =  base_folder + processed_text
    createFolder()

    #Code for hippo campus
    s=strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    line = (text.upper()+ ',' +base_folder+text.upper() +','+s)
    fd = open('/home/pi/owl.csv','a')
    fd.write(line+"\n")
    fd.close()

    def my_form():
        try:
            global wifis
            local_wifis = get_wifis()
            wifis = []
            return render_template( "index.html",wifi_avail=local_wifis,wifi_conn=check_wifi())
        except:
            return redirect(url_for('my_form'))

    #Ip address and port number input is accepted here
    #@app.route('/my_form_copy', methods = ['POST'])
    def my_form_copy():
        try:
            source = ''
            global processed_text
            button = request.form["ipbutton"]
            print button
            if button == "Copy":
                #input for IP and PORT Number into 'HOST' and 'PORT' variable
                #HOST = request.form['ipaddr']
                #PORT = int(request.form['port'])
                #converting input text to upper case for final MR number
                d = datetime.datetime.now()
                processed_text = str(d.year)+'-'+str(d.month)+'-'+str(d.day)+'/'+text.upper() + '/images/'
                source = base_folder + processed_text
                obj_fc.copy_files(HOST,PORT,source)
                #return redirect(url_for('captureSimpleFunc'))
                return redirect(url_for('my_form'))
            else:
                return redirect(url_for('my_form_post'))
        except:
            return redirect(url_for('my_form'))

    print '3'
    #MR number input is accepted here
    #@app.route('/', methods = ['POST'])
    def my_form_post():
        #processesd_text stores the MR_number
        global processed_text
        global obj_state
        global last_img
        # global variable is used to get the MR number while copy
        global text
        obj_state = True
        normalON()
        button = request.form['my-form'].strip()
        #for Refresh button
        if button == "":
            global wifis
            local_wifis = get_wifis()
            wifis = []
            return render_template('index.html',wifi_avail=local_wifis,wifi_conn=check_wifi())
        #for Shutdown button
        if button == "S":
            shut_down()
            return render_template('capture_simple.html', params=tokens, grades={})
        #for Send button
        if button == "Send":
            #input for MR Number into 'text' variable
            text = request.form['text']
            wifi_name = request.form['wifi_name'].strip()
            wifi_password = request.form['password'].strip()

        #print 'wifi',wifi_name,wifi_password
        # connect to wifi
        #os.popen("sudo ifconfig wlan0 up")
        #print 'popen success'
	#cells = wifi.Cell.all('wlan0')
	#print 'before if'
        #if (wifi_name != "") and (wifi_password != ""):
	    #print 'entered if'
            #connect_wifi(wifi_name,wifi_password)
	    #print 'connect success'
            #Delete WiFi from auto connect list
            #Delete(wifi_name)
	    #print 'delete success'
        #converting input text to upper case for final MR number
        processed_text = text.upper()
        #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d = datetime.datetime.now()
        processed_text = str(d.year)+'-'+str(d.month)+'-'+str(d.day)+'/'+text.upper() + '/images/'
        source =  base_folder + processed_text
        # Code for hippo campus
        s=strftime("%Y-%m-%d_%H:%M:%S", gmtime())
        line = (text.upper()+ ',' +base_folder+text.upper() +','+s)
        fd = open('/home/pi/owl.csv','a')
        #fd.write(base_folder+text.upper())
        fd.write(line+"\n")
        fd.close()
        #make_a_dir(processed_text)

        #declaring object Fundus_cam
        global obj_fc
        obj_fc = Fundus_Cam()
        return redirect(url_for('captureSimpleFunc'))



    #captureSimple : to display simple image
    #@app.route('/captureSimple', methods=['GET','POST'])
    def captureSimpleFunc(d):
        try:
            global last_img
            global grade_val
            global no
            global text
            global event1
            global event2
            global event3
            global event4
            global event5
            global obj_fc
            #if request.method == 'GET':
                #return render_template('capture_simple.html', params=tokens, grades={})
            #if request.method == 'POST':
                #if "d" in request.form.keys():
                    #d=request.form['d']

                    #if photo has to be taken
            if d == 'Click':
		flag = 0
                enable = 0
                event2.clear()
                event1.clear()
                event3.set()
                #obj_fc.capture()
                #decode_image(obj_fc.image)
                #threeLed()
                fourLed()
                #time.sleep(0.01)
                return 1
                #return render_template('capture_simple.html', params=tokens, grades={})

		#If flip button pressed
            if d == 'Flip':
                print '6'
		flag = 0
                event1.clear()
                #obj_fc.flip_cam()
                pygame.display.flip()
		return 1
                #return render_template('capture_simple.html', params=tokens, grades={})


                    #if 'Video' has to be taken and 'Vid' button is pressed
            if d == 'Vid':
		flag = 0
                event1.clear()
                #obj_fc.continuous_capture()
                #decode_image(obj_fc.images)
                print 'vid clicked'
                #print no
                a = no-2
                b = no-1
                f1 = (base_folder+processed_text+str(a)+'.jpg')
                #print f1
                f2 = (base_folder+processed_text+str(b)+'.jpg')
                f3 = (base_folder+processed_text+str(no)+'.jpg')
                print 'file names given'
                stitched_image = stitch(f1,f2,f3)
                print 'exited stitch'
                cv2.imwrite(base_folder+processed_text+'stitched_'+str(no/3)+'.jpg', stitched_image)
		return 1
                #return render_template('capture_simple.html', params=tokens, grades={})

                    #if photo has to be taken
            #if d == grade_val:
	    if d == 'Grade':
                print('entered grade loop')
		flag = 0
                event1.clear()
                event3.clear()
                if last_img == '1':
		    return -1
                    #return render_template('capture_simple.html', params=tokens, grades={'grade':'NO IMAGE SPECIFIED'})

                if last_img != '1':
                    # grading_val(last_img)
                    #event1.set()
                    if(event4.is_set()):
                        try:
                            print 'last_img!=1'
                            print no
                            print last_img
                            obj_fc.stop_preview()
                            obj_fc.stop()
                            event2.set()
                            grade_val = str(grade(last_img+str(no)+'.jpg'))[:4]
                            print "the grade is " + grade_val
                            #f11=open('/home/pi/openDR/grade.txt',"wb")
                           # f11.write(gd)
                           # f11.close()
		            return grade_val
                        except:
                            os.system('sudo python /home/pi/openDR/Owl-GUI.py')
                    elif(event5.is_set()):
                        obj_fc.stop_preview()
                        obj_fc.stop()
                        #screen.blit(text_warning,(400,200))
                        #pygame.display.update()
                        #time.sleep(2)
                        #screen.fill(white,(400,200,200,30))
                    #return render_template('capture_simple.html', params=tokens, grades={'grade':grade_val})


                    #if stop button is pressed
	    if d == 'Switch':
		flag = 0
                event1.clear()
		print 'bro in switch'
                #if obj_state == True:
                print '8'
                if (event2.is_set()):
                    print('event2 is set yo')
                    #obj_fc.stop_preview()
                    #obj_fc.stop()
                    event2.clear()
                    pygame.quit()
                    os.system("sudo python /home/pi/openDR/Owl-GUI.py")
                else:
                    try:
                        print('tried')
                        obj_fc.stop_preview()
                        obj_fc.stop()
                        pygame.quit()
                        os.system("sudo python /home/pi/openDR/Owl-GUI.py")
                    except:
                        print('except')
                        pygame.quit()
                        os.system("sudo python /home/pi/openDR/Owl-GUI.py")
                #return 1
                #return redirect(url_for('my_form'))

                    #if copy button pressed
            if d == 'Copy':
		flag = 0
                event1.clear()
                #if obj_state == True:
                obj_fc.stop_preview()
                obj_fc.stop()
                #commandline = 'sudo python /home/pi/client.py'
                #os.system(client.py)
		return 1
                #return render_template('ip_address.html')

            if d == 'Shut':
		flag = 0
                event1.clear()
                shut_down()
		return 1
                #return render_template('capture_simple.html', params=tokens, grades={})

            if d == 'Start':
		#flag = 0
                event2.clear()
                event1.clear()
                obj_fc = Fundus_Cam()
                #obj_fc.start_prev()
		return 1
                #return render_template('capture_simple.html', params=tokens, grades={})

        except:
	    print 'lol you are dead'
            os.system('sudo python /home/pi/openDR/Owl-GUI.py')
            if obj_fc:
                obj_fc.stop_preview()
                obj_fc.stop()
	    return -2
            #return redirect(url_for('my_form'))

    def threeLed():
        led3 = []
        led3.append([led[0],led[4],led[8]])
        led3.append([led[1],led[5],led[9]])
        led3.append([led[2],led[6],led[10]])
        led3.append([led[3],led[7],led[11]])
        for i in range(0,4):
            GPIO.setup(led3[i],GPIO.OUT)
            GPIO.output(led3[i],GPIO.HIGH)
            obj_fc.capture()
            Thread(target=decode_image,args=(obj_fc.image,)).start()
            #decode_image(obj_fc.image)
            GPIO.output(led3[i],GPIO.LOW)
        GPIO.output(led3[0],GPIO.HIGH)

    def fourLed():
        led4 = []
        led4.append([led[0],led[3],led[6],led[9]])
        led4.append([led[1],led[4],led[7],led[10]])
        led4.append([led[2],led[5],led[8],led[11]])
        for i in range(0,3):
            GPIO.setup(led4[i],GPIO.OUT)
            GPIO.output(led4[i],GPIO.HIGH)
            obj_fc.capture()
            Thread(target=decode_image,args=(obj_fc.image,)).start()
           #decode_image(obj_fc.image)
            GPIO.output(led4[i],GPIO.LOW)
        GPIO.output(led4[0],GPIO.HIGH)

    # A seperate function for getting the value from theia and assigning it to grade_val
    def grading_val(last_img):
        try:
            global grade_val
            grade_val = str(grade(last_img))
            print "the grade is " + grade_val
            pass
        except:
            if obj_fc:
                obj_fc.stop_preview()
                obj_fc.stop()
            return redirect(url_for('my_form'))




    def decode_image(images):
        #name=raw_input("enter the name to be saved")
            global no
            global last_img
            global grade_val
            #no=0
            ## This part of code is to open the file 'name' and add the number
            #  in the file to the pic taken and increment it
            ## This is done so that each pic taken has a unique name and also no
            #  overwriting happens
            #file_r = open(base_folder + '/name','r')
            #picn = (int)(file_r.read())
            #picn = picn+1
            #file_r.close()
            #file_w = open(base_folder + '/name','w')
            #file_w.write(str(picn))
            #file_w.close()
            global text
            up_text = text.upper()

            d = datetime.datetime.now()
            last_img = (base_folder
                                   + processed_text
                                   )

            # Save image in the particular directory with the given file name
            if type(images) is list:
                print 'entered if'
                for img in images:
                    image=cv2.imdecode(img,1)
                    image=extract_fundus(image)
                    cv2.imwrite( last_img, image )
                    no=no+1
            else:
                image=cv2.imdecode(images,1)
                #image=extract_fundus(image)
                while True:
                    no = no + 1
                    #print no
                    if not os.path.isfile(last_img + str(no) + '.jpg'):
                        cv2.imwrite( last_img + str(no) + '.jpg',image )
                        break
    #-------------------Flask implementation ends here--------------------#

    #--------------NO MAN'S LAND. ABANDON ALL HOPE YE WHO ENTER-----------#

    #......Below this line, all the functions not having flask lie.....#


    #make a directory of patient's name if it does not exist



    # Set the pins
    # Names are based on the colours of the wires connecting to the LEDs
    # NOTE: Both the orangeyellow and bluegreen
    #       LEDs are active LOW, hence 0 is ON and vice versa
    #orangeyellow = 14
    #bluegreen  = 15
    switch = 4
    i=1 # initial_counter

    # pi is initialized as the pigpio object
    #pi=pigpio.pi()
    #pi.set_mode(orangeyellow,pigpio.OUTPUT)
    #pi.set_mode(bluegreen,pigpio.OUTPUT)
    #pi.set_mode(switch,pigpio.INPUT)
    #set a pull-up resistor on the switch pin
    #pi.set_pull_up_down(switch,pigpio.PUD_UP)
    # Defining functions for putting off each LED
    def normalON():

        GPIO.setwarnings(False)
        GPIO.output(defaultOn,GPIO.HIGH)
        #global orangeyellow
        #global bluegreen
        # orangeyellow is ON and the other is OFF
        #pi.write(orangeyellow,0)
        #pi.write(bluegreen,1)

    #def secondaryON():
        # toggle
        #pi.write(orangeyellow,1)
        #pi.write(bluegreen,0)


    # if scheme already exixts, activate it
    def FindFromSavedList(ssid):
        print 'inside FindFromSavedList',ssid
        try:
            cell = wifi.Scheme.find('wlan0', ssid)
        except wifi.exceptions.InterfaceError:
            os.popen("sudo ifconfig wlan0 up")
            cells = wifi.Cell.all('wlan0')
            cell = wifi.Scheme.find('wlan0', ssid)
        if cell:
            return cell
        return False



    # Delete the refrence of the scheme from interfaces file
    def Delete(ssid):
        if not ssid:
            return False
        cell = FindFromSavedList(ssid)
        os.popen("sudo ifconfig wlan0 up")
        cell = wifi.Scheme.find('wlan0', ssid)
        if cell:
            cell.delete()
            print 'deleting ..',cell
            return True
        return False

    #Connect to wifi wnal0 maybe down,
    #so bring it up before connecting
    def Connect(ssid, password=None):
        print 'connect',ssid
        try:
            os.popen("sudo ifconfig wlan0 up")
	    print 'connect popen success'
            cells = wifi.Cell.all('wlan0')
	    print cells
	    print 'cells'
            cell = next((x for x in cells if x.ssid == ssid),None)
            print 'cell'
	    print password
            scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
            #if already saved, activate that scheme
            savedcell = FindFromSavedList(cell.ssid)
            if savedcell:
                scheme = savedcell
            else:
                scheme.save()
                print("scheme saved",scheme)

            os.popen("sudo ifconfig wlan0 up")
            cells = wifi.Cell.all('wlan0')
            os.popen("sudo ifconfig wlan0 up")
            scheme.activate()
            #Delete(ssid)
        except requests.exceptions.RequestException:
            print "inside Connection error. try connecting again"
            Delete(ssid)
            Connect(ssid,password)#try connecting again
        except:
            print 'inside exception 1'
            print traceback.print_exc()
            Delete(ssid)
            Connect(ssid,password)#try connecting again


    #get a list of available wifis
    def get_wifis():
        os.popen("sudo ifconfig wlan0 up")
        stream = os.popen("sudo iwlist wlan0 scan")
        global wifis
        global networksfound

        for line in stream:
            if "ESSID" in line:
                networksfound += 1
                tmp = " " + line.split('ESSID:"', 1)[1].split('"', 1)[0]
                if networksfound == 1:
                    wifis = []
                    wifis = [tmp]
                else:
                    wifis.append(tmp)
        if networksfound == 0:
            print "No networks found in this area. Exiting..."
        #reset the value to zero
        networksfound = 0
        return wifis



   #main method that connects and deletes the wifi connection
    def connect_wifi(name,pssd):
        os.popen("sudo ifconfig wlan0 up")
        cells = wifi.Cell.all('wlan0')
        if (name != "") and (pssd != ""):
            Connect(name,pssd)
            print 'connected......'
            # Delete WiFi from auto connect list
            Delete(name)
            return 'connected......'

    # to check if currently connected to any wifi
    def check_wifi():
        wifi = Wireless('wlan0')
        if wifi.getAPaddr() == "00:00:00:00:00:00":
            return "No WiFi"
        else:
            return wifi.getEssid()



#exception module not working as desired
except :
    e = sys.exc_info()[0]
    #write_to_page( "<body>Error occured: We will now shut down <p>%s</p></body>" % e )

    #wait for 3 seconds
    time.sleep(3)
    #call shutdown function
    shut_down()

#function pipes the 'shutdown now' command to terminal
def shut_down():
        command = "/usr/bin/sudo /sbin/shutdown now"
        import subprocess
        process=subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output


def upd():
    #pygame.init()
    global grade_val
    global event1
    global event3
    global check_wifi
    name = ""
    temp = ""
    name1=""
    global gd
    font = pygame.font.SysFont(fontStyle, 20)
    ctr=0
    count = 0
    #screen.fill(black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(logo_resized,(300,30))
        cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True,
                           stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'off/any' in line:
                event4.clear()
                event5.set()
               # screen.fill((0,0,0),(25,30,32,24))
                screen.fill((255,255,255),(750,50,32,24))
                screen.blit(wifiDisConnec,(750,50))
               # event1.clear()
            elif 'Link Quality' in line:
                check_wifi=1
                #screen.fill(white,(400,200,200,30))
                event5.clear()
                event4.set()
                screen.fill((255,255,255),(750,50,32,24))
                screen.blit(wifiConnec,(750,50))


        if(event1.is_set()):
            text_2 = font.render('Grade:', 0,(0,0,0))
            text_3 = font.render(gd, 0,(0,0,0))
            screen.blit(text_2,(150,250))
            screen.blit(text_3,(150,290))
        if(event3.is_set()):
            screen.fill(white,(150,290,100,50))


        Flip("Flip",3,3,100,60,olive,chocolate)
        Capture("Capture",0,60,100,60,olive,chocolate)
        Grade("Grade",0,120,100,60,olive,chocolate)
       # Start("Start",0,180,100,60,olive,chocolate)
        Video("Stitch",0,240,100,60,olive,chocolate)
       # Copy("Copy",0,300,100,60,olive,chocolate)
        Back("Back",0,360,100,60,olive,chocolate)
        Connect_wifi("",750,50,30,30,olive,chocolate)
        pygame.display.flip()
    return name1

def upd_flip():
    #pygame.init()
    global grade_val
    global event1
    global event3
    global gd
    global enable
    global event4
    global event5
    global check_wifi
    name = ""
    temp = ""
    name1=""
    font_1 = pygame.font.SysFont(fontStyle, 20)
    ctr=0
    count = 0
   # screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
   # screen1.fill(black)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True,
                           stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'off/any' in line:
                event4.clear()
                event5.set()
                screen1.fill((255,255,255),(50,420,32,24))
                screen1.blit(wifiDisConnec_rot,(50,420))
               # event1.clear()
            elif 'Link Quality' in line:
                check_wifi = 1
               # screen1.fill(white,(400,200,200,30))
                event5.clear()
                event4.set()
                screen1.fill((255,255,255),(50,420,32,24))
                screen1.blit(wifiConnec_rot,(50,420))


        text_g = font_1.render("Grade:", True, (0,0,0))
        text_g = pygame.transform.rotate(text_g, 180)
        text_3 = font_1.render(gd, 0,(0,0,0))
        text_3 = pygame.transform.rotate(text_3, 180)
        screen1.blit(logo_rot,(300,350))
        Flip1("Flip",700,420,100,60,olive,chocolate)
        Capture1("Capture",700,360,100,60,olive,chocolate)
        Grade1("Grade",700,300,100,60,olive,chocolate)
       # Start1("Start",700,240,100,60,olive,chocolate)
        Video1("Stitch",700,180,100,60,olive,chocolate)
      #  Copy1("Copy",700,120,100,60,olive,chocolate)
        Back1("Back",700,60,100,60,olive,chocolate)
        Connect_wifi("",50,420,30,30,olive,chocolate)
        if(event1.is_set()):
            #text_g = font_1.render("Grade:", True, (0,0,0))
            #text_g = pygame.transform.rotate(text_g, 180)
            #screen.blit(text, [30, 0])
            #text_3 = font_1.render(gd, 0,(0,0,0))
            #text_3 = pygame.transform.rotate(text_3, 180)
            screen1.blit(text_g,(330,230))
            screen1.blit(text_3,(330,190))
            pygame.display.update()
        if(event3.is_set()):
            screen1.fill(white,(330,190,100,35))
            event3.clear()
            #pygame.display.update()

        pygame.display.flip()

    return name1


def Flip(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    global var_flip
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,0,100,60))
        screen.blit(text_flip,(10,10))
        if click[0] == 1 and action ==None and flag==1:
            var_flip=var_flip+1
            if(var_flip%2==1):
                #pygame.quit()
                #pygame.init()
               # screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
                screen1.fill(black)
                upd_flip()
                flag = captureSimpleFunc('Flip')
                screen1.fill(black)
                pygame.display.flip()
            elif(var_flip%2==0):
                screen.fill(black)
                upd()
                flag = captureSimpleFunc('Flip')
                screen.fill(black)
                pygame.display.flip()
    else:
        screen.fill((180,180,180),(0,0,100,60))
        screen.blit(text_flip,(10,10))

def Video(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,240,100,60))
        screen.blit(text_vid,(10,250))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0
            flag= captureSimpleFunc('Vid')
            #pygame.quit()
    else:
        screen.fill((180,180,180),(0,240,100,60))
        screen.blit(text_vid,(10,250))

def Capture(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global enable
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,60,100,60))
        screen.blit(text_cap,(10,70))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0
            #time.sleep(1)
            screen.fill((255,255,255),(749,99,15,15))
            screen.fill((255,0,0),(750,100,10,10))
            flag=captureSimpleFunc('Click')
            enable = flag
            #if(flag==1):
               # screen.fill((255,255,255),(750,100,10,10))
    else:
        screen.fill((180,180,180),(0,60,100,60))
        screen.blit(text_cap,(10,70))

def Copy(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,300,100,60))
        screen.blit(text_copy,(10,310))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0
            captureSimpleFunc('Copy')

    else:
        screen.fill((180,180,180),(0,300,100,60))
        screen.blit(text_copy,(10,310))

def Grade(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global gd
    global enable
    global clickButton
    global event4
    global event5
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,120,100,60))
        screen.blit(text_grd,(10,130))
        if click[0] == 1 and action ==None and flag==1 and enable==1 and check_wifi==1:
            #flag=0
            screen.fill((255,255,255),(749,99,15,15))
            gd = captureSimpleFunc('Grade')
            print 'entered grade button'
            print gd

            if(event4.is_set()):
                f11=open('/home/pi/openDR/grade.txt',"wb")
                f11.write(gd)
                f11.close()
                os.system('sudo python /home/pi/openDR/Owl-Grade.py')
            flag=1
            event1.set()

    else:
        screen.fill((180,180,180),(0,120,100,60))
        screen.blit(text_grd,(10,130))

def Start(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,180,100,60))
        screen.blit(text_strt,(10,190))
        if click[0] == 1 and action ==None and flag==1:
             print 'its empty duuude!'
             #flag=0
             flag=captureSimpleFunc('Start')
             time.sleep(0.01)

    else:
        screen.fill((180,180,180),(0,180,100,60))
        screen.blit(text_strt,(10,190))

def Back(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen.fill((33,78,99),(0,360,100,60))
        screen.blit(text_back,(10,370))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0
            captureSimpleFunc('Switch')
    else:
        screen.fill((180,180,180),(0,360,100,60))
        screen.blit(text_back,(10,370))



def Video1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,180,100,60))
        screen1.blit(video_rot,(710,190))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0
            flag= captureSimpleFunc('Vid')
            #pygame.quit()
    else:
        screen1.fill((180,180,180),(700,180,100,60))
        screen1.blit(video_rot,(710,190))

def Capture1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,360,100,60))
        screen1.blit(cap_rot,(710,370))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0

            screen1.fill((255,255,255),(26,299,15,15))
            screen1.fill((255,0,0),(25,300,10,10))
            flag=captureSimpleFunc('Click')
            enable = flag
            #if(flag==1):
                #screen.fill((255,255,255),(25,300,10,10))
    else:
        screen1.fill((180,180,180),(700,360,100,60))
        screen1.blit(cap_rot,(710,370))

def Copy1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,120,100,60))
        screen1.blit(copy_rot,(710,130))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0
            captureSimpleFunc('Copy')

    else:
        screen1.fill((180,180,180),(700,120,100,60))
        screen1.blit(copy_rot,(710,130))

def Grade1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global gd
    global clickButton
    global event4
    global event5
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,300,100,60))
        screen1.blit(grade_rot,(710,310))
        if click[0] == 1 and action ==None and flag==1 and enable==1 and check_wifi==1:
            #flag=0
            screen1.fill((255,255,255),(26,299,15,15))
            gd = captureSimpleFunc('Grade')
            print 'entered grade button'
            print gd
            if(event4.is_set()):
                f11=open('/home/pi/openDR/grade.txt',"wb")
                f11.write(gd)
                f11.close()
                os.system('sudo python /home/pi/openDR/Owl-Grade.py')
            flag=1
            event1.set()

    else:
        screen1.fill((180,180,180),(700,300,100,60))
        screen1.blit(grade_rot,(710,310))

def Start1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,240,100,60))
        screen1.blit(start_rot,(710,250))
        if click[0] == 1 and action ==None and flag==1:
             print 'its empty duuude!'
             #flag=0
             flag=captureSimpleFunc('Start')

    else:
        screen1.fill((180,180,180),(700,240,100,60))
        screen1.blit(start_rot,(710,250))

def Back1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,60,100,60))
        screen1.blit(back_rot,(710,70))
        if click[0] == 1 and action ==None and flag==1:
            #flag=0and enable==1
            captureSimpleFunc('Switch')
    else:
        screen1.fill((180,180,180),(700,60,100,60))
        screen1.blit(back_rot,(710,70))

def Flip1(msg,x,y,w,h,ic,ac,action=None):
    global flag
    global clickButton
    global var_flip
    #screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
    #screen1.fill(black)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        screen1.fill((33,78,99),(700,420,100,60))
        screen1.blit(flip_rot,(710,430))
        if click[0] == 1 and action ==None and flag==1:
            var_flip=var_flip+1
            if(var_flip%2==1):
                #pygame.quit()
                #pygame.init()
               # screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
                screen1.fill(black)
                upd_flip()
                flag = captureSimpleFunc('Flip')
                pygame.display.flip()
            elif(var_flip%2==0):
                screen.fill(black)
                upd()
                flag = captureSimpleFunc('Flip')
                screen.fill(black)
                pygame.display.flip()
    else:
        screen1.fill((180,180,180),(700,420,100,60))
        screen1.blit(flip_rot,(710,430))

# to create textobjects
def text_objects(text,font):
    textSurface = font.render(text, True,(0,0,0))
    return textSurface,textSurface.get_rect()

def Connect_wifi(msg,x,y,w,h,ic,ac,action=None): 
    global event2 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action ==None:
            #screen.fill(((34,63,76)),(25,30,30,22))
            screen.fill(((0,0,0)),(25,30,30,22))
            #screen.blit(wificlk,(25,30))
            if(event2.is_set()):
                pygame.quit()
                execute = ("sudo python /home/pi/openDR/Owl-wifi.py")
                os.system(execute)
            else:
                try:
                    obj_fc.stop_preview()
                    obj_fc.stop()
                   # pygame.quit()
                    os.system("sudo python /home/pi/openDR/Owl-wifi.py")
                except:  
                   # pygame.quit()
                    os.system("sudo python /home/pi/openDR/Owl-wifi.py")            
                  
                
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Display WLAN signal strength.')
    parser.add_argument(dest='interface', nargs='?', default='wlan0',
                    help='wlan0 interface (default: wlan0)')
    args = parser.parse_args()
    upd()
    os.system("sudo pkill -9 -f /home/pi/openDR/Owl-GUI.py")
    os.system("sudo pkill -9 -f /home/pi/openDR/Owl-wifi.py")
    #app.run(host='0.0.0.0')

