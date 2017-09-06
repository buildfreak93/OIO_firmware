
#!/usr/bin/python

import pygame
import time
import random
#import pygame.camera
import os
import sys
import serial
pygame.init()
from multiprocessing import Process, Queue, Event
from PIL import Image
from datetime import datetime

import datetime
import vkeyboard

from pygame.locals import *
from vkeyboard import *
import subprocess

import argparse


global event1
global event2
global event3

event1 = Event()
event2 = Event()
event3 = Event()
#from Led import *
#from Led import LedOn



#a = LedOn()
#indicator = ""
#indicator=a.battery()
#print(indicator)

datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
time_stamp = datetime.datetime.now().strftime("%Y_%m_%d")
print(time_stamp)
fontStyle = "helvetica"
fontSize = 20

display_width = 800
display_height = 480

text_width=400
text_height=160

width=100
height=50

black = (0,0,0)
white= (255,255,255)

pos1_x=0
pos2_x=700
pos_y=400

msg_1=""
msg_2="Next"

#chocolate=(210,105,30)
#chocolate=(108,110,104)
chocolate=(180,180,180)
khaki=(240,230,140)
olive=(180,180,180)
#olive=(187,225,65)

screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('OWL')
clock = pygame.time.Clock()
text=""

# to store the timestamp
f12 = open('/home/pi/openDR/timestamp.txt',"wb")
f12.write(time_stamp)
f12.close()

size=(30,22)
size_Sdwn=(30,30)

wifiConnec = pygame.image.load('/home/pi/openDR/wifi.png')
wifiDisConnec=pygame.image.load('/home/pi/openDR/wifi_disabled.png')

plot = pygame.image.load('/home/pi/openDR/wifi.png')
powerBtn=pygame.image.load('/home/pi/openDR/powerbutton-01.png')
logo=pygame.image.load('/home/pi/openDR/owlLogo.jpg')
next_Btn=pygame.image.load('/home/pi/openDR/next.png')
mrnumber=pygame.image.load('/home/pi/openDR/mrnumber.png')
wificlk=pygame.image.load('/home/pi/openDR/wifiwhite.png')

plot_resized = pygame.transform.scale(plot,size)
powerBtn_resized = pygame.transform.scale(powerBtn,size_Sdwn)
logo_resized=pygame.transform.scale(logo,(200,100))

#screen.fill((34,63,76))
screen.fill(black)
screen.blit(plot_resized,(25,30))
screen.blit(powerBtn_resized,(750,30))
screen.blit(logo_resized,(300,30))
screen.blit(next_Btn,(750,185))
screen.blit(mrnumber,(100,90))

#pygame.draw.rect(screen, (180,180,180),
                   #(0,0,800,480), 3)
pygame.draw.line(screen,(0,0,0),(0,240),(800,240),8)

 

def consumer(text):
    font = pygame.font.SysFont("Roboto", 50)
    block = font.render(text, True,olive) 
    screen.blit(block,(300,text_height))
    #pygame.display.update()
    screen.fill((0,0,0),(300,160,400,70)) 
    screen.blit(block,(300,text_height)) 
    pygame.display.update()   
    print(len(text))
    print(text)
    if(len(text) >= 1):
        f11=open('/home/pi/openDR/next.txt',"wb")
        f11.write(text)
        f11.close()
    return text 


def name(event1,event2):
    pygame.init()
    font = pygame.font.SysFont(fontStyle, fontSize)
    font1 = pygame.font.SysFont(fontStyle, 20)
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(screen, consumer, layout)
    keyboard.enable()
    keyboard.draw()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            keyboard.on_event(event)            
            if event.type == QUIT:
                pygame.quit()
                running = False  
        current_time = time.ctime()
        font = pygame.font.SysFont(fontStyle, fontSize)
        time_date = font.render(current_time, 0,(146,148,151)) 
       # screen.fill((0,0,0),(450,10,170,15))
        screen.blit(time_date,(500,30))
        screen.fill((0,0,0),(500,30,220,30))
        screen.blit(time_date,(500,30))
        if(event1.is_set()):
            screen.fill((0,0,0),(25,30,32,24))
            screen.blit(wifiDisConnec,(25,30))
            event1.clear()

        elif(event2.is_set()):
            screen.fill((0,0,0),(25,30,32,24))
            screen.blit(wifiConnec,(25,30))
            event2.clear()

        button(msg_2,750,176,21,48,olive,chocolate)
        button1(msg_1,750,30,30,30,olive,chocolate)
        button2("Next",25,30,30,22,olive,chocolate)

        pygame.display.flip()

def get_wifi(event1,event2):
    while True:
        cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True,
                           stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'off/any' in line:
                event1.set()
            elif 'Link Quality' in line:
                event2.set()


	
def text_objects(text,font):
    textSurface = font.render(text, True,black)
    return textSurface,textSurface.get_rect()

def text_objects_1(text,font):
    textSurface = font.render(text, True,chocolate)
    return textSurface,textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None): 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            print("success")
            pygame.quit()
            execute = ("sudo python /home/pi/openDR/fundus_v4.py")
            os.system(execute) 
	    #pygame.quit() 
   # else:
        #pygame.draw.rect(screen, ic,(x,y,w,h))

   # smallText = pygame.font.SysFont(fontStyle,fontSize)
   # textSurf, textRect = text_objects(msg, smallText)
   # textRect.center = ( (x+(w/2)), (y+(h/2)) )
   # screen.blit(textSurf, textRect)

 

def button1(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            print("shutting down")
            pygame.quit()
            #os.system('sudo poweroff')
            
            os.system("sudo pkill -9 -f Owl-GUI.py")  
            #os.system('sudo poweroff')                      
            

def button2(msg,x,y,w,h,ic,ac,action=None):  
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action ==None:
            #screen.fill(((34,63,76)),(25,30,30,22))
            screen.fill(((0,0,0)),(25,30,30,22))
            screen.blit(wificlk,(25,30))
            pygame.quit() 
            execute = ("sudo python /home/pi/openDR/Owl-wifi.py")
            os.system(execute)
	    #pygame.quit()
  

#function pipes the 'shutdown now' command to terminal

if __name__ == "__main__":

    #os.system("sudo pkill -9 -f /home/pi/openDR/startscreen.py")
     #os.system("sudo pkill -9 -f /home/pi/opnDR/fundus_v4.py")
    os.system("sudo pkill -9 -f startscreen.py")
    os.system("sudo pkill -9 -f fundus_v4.py")
    os.system("sudo pkill -9 -f Fundus_Cam.py")

    #pygame.init()        
    pygame.init()        

    parser = argparse.ArgumentParser(description='Display WLAN signal strength.')
    parser.add_argument(dest='interface', nargs='?', default='wlan0',
                    help='wlan0 interface (default: wlan0)')
    args = parser.parse_args()

    p1 = Process(target=name, args=(event1,event2,))
    p2 = Process(target=get_wifi, args=(event1,event2,))

    p1.start()
    p2.start()

    
    p1.join()
    print("p2 joined")    
    p2.join() 
