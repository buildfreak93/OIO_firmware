
#append the functionality in the button function definition
import pygame
import time
import random
import os
import sys
import csv
import pygame.camera
import datetime
import serial
import wireless

from multiprocessing import Process, Queue, Event
from PIL import Image
from pygame.locals import *
from datetime import datetime
from sys import *
from wireless import Wireless
import vkeyboard
from pygame.locals import *
from vkeyboard import *

os.system("sudo iwlist wlan0 scan | grep ESSID > network.txt")

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

event1 = Event()
event2 = Event()
event3 = Event()
#global lines_4
global clickButton

display_width = 800
display_height = 480

black = (0,0,0)
white= (255,255,255)

blanchedalmond=(180,180,180)
chocolate=(180,180,180)
khaki=(240,230,140)
#olive=(128,128,0)
olive=(96,96,96)

#Initialization
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
screen.fill((0,0,0))
screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
screen1.fill((0,0,0))
pygame.display.set_caption('wifi')
clock = pygame.time.Clock()

font_1 = pygame.font.SysFont("Helvetica", 20)
text_1 = font_1.render("available networks", 0,(180,180,180)) 
screen.blit(text_1,(10,10))


ch = []
text = ['']
lines_4 = []

f11 = open("network.txt","r")
lines_1 = f11.readlines()
f11.close()

f11 = open("network.txt","r")
lines = len(f11.readlines())

for i in range(lines):   
    ch.append(lines_1[i])    
f11.close() 

x_cord = 100
y_cord = 10
width = 56
height = 20
text_x_cord = 20
text_y_cord = 60
count = 0
name1=""


class Finder:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}

    def run(self):
        #command = """sudo iwlist wlx18d6c71c04b2 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        command = """sudo iwlist wlan0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen(command.format(self.server_name))
        result = list(result)

        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print ssid_list
            print("Successfully get ssids {}".format(str(ssid_list)))

        for name in ssid_list:
            try:
                print(name)
                print("entered try")
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print(name)
                    print("Successfully connected to {}".format(name))

    def connection(self, name):
        try:
            os.system("sudo nmcli d wifi connect '{}' password {} iface {}".format(name,
       self.password,
       self.interface_name))
        except:
            raise
        else:
            return True    
    
def upd(event1,event2,event3):
    pygame.init()
    name = ""
    temp = ""
    name1=""
    font = pygame.font.SysFont(fontStyle, 20)
    text_1 = font.render("Available wifi networks", 0,(180,180,180)) 
    ctr=0
    count = 0
    screen.fill((0,0,0))

    while True: 
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                temp = evt.unicode
                if evt.unicode.isalnum():
                    name += evt.unicode
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == K_RETURN:
                   # event1.set()
                    print("event is set")
                    name1 = name
		    break                  
            elif evt.type == QUIT:
                return    
        text_2 = font.render(name, 0,(180,180,180))
        text_3 = font.render("Password:", 0,(180,180,180))
        Esc("Esc",700,400,100,50,olive,chocolate)
        for line in lines_1:
            line =line.strip()
            words,networks,null=line.split('"')
            lines_4.append(networks.strip())

        if count != lines:
            for i in range(lines): 
                button(lines_4[i],30,(text_y_cord+ctr),300,35,olive,chocolate,i)
                ctr=ctr+50
                count = count + 1
                pygame.display.flip() 
                pygame.display.update()
        ctr=0
        for i in range(lines): 
            button(lines_4[i],30,(text_y_cord+ctr),300,35,olive,chocolate, i)
            pygame.display.flip() 
            pygame.display.update()
            ctr=ctr+50
        if(event2.is_set()):
            screen1 = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
            screen1.fill((0,0,0))
            pygame.display.set_caption('Pupil+')
            main()
            loop() 
            upd1()           
    return name1

def consumer(text):
    font = pygame.font.SysFont("Helvetica", 30)
    block = font.render(text, True,olive) 
    screen.blit(block,(300,text_height))
    #pygame.display.update()
    screen.fill((0,0,0),(300,160,400,56)) 
    screen.blit(block,(300,text_height)) 
    pygame.display.update()   
    print(len(text))
    print(text)
    if(len(text) >= 1):
        f11=open('key.txt',"wb")
        f11.write(text)
        f11.close()
    return text 
    
 
def main():
    global event3
    pygame.init()
    font = pygame.font.SysFont(fontStyle, fontSize)
    layout = VKeyboardLayout(VKeyboardLayout.AZERTY)
    keyboard = VKeyboard(screen1, consumer, layout)
    keyboard.enable()
    keyboard.draw()
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            keyboard.on_event(event)
            Connect(msg_1,700,400,100,50,olive,chocolate)
            Back("Back",0,400,100,50,olive,chocolate)
            if event.type == QUIT:
                running = False  

        content = font.render("Enter the password", True,olive)
        screen1.blit(content,(50,30))

def upd1():
    global event3
    for line in lines_1:
        line =line.strip()
        words,networks,null=line.split('"')
        lines_4.append(networks.strip())
    if(event3.is_set()):
        print("reached")
        print clickButton
        f11 = open("key.txt","r")
        key = f11.readline()
        f11.close    
        F = Finder(server_name=lines_4[clickButton],
           password=key,
           #interface="wlx18d6c71c04b2")
               interface="wlan0")
        F.run()
        pygame.quit()
        #os.system("sudo python fundus_v3.py")

def loop():
    #temp1 = name()
    pygame.init()
    font = pygame.font.SysFont(fontStyle, fontSize)
    while True:
        content = font.render("Enter the password", True,olive)
        screen1.blit(content,(50,30))
        Connect(msg_1,700,400,100,50,olive,chocolate)
        Back("Back",0,400,100,50,olive,chocolate)
        pygame.display.flip()


def button(msg,x,y,w,h,ic,ac, i,action=None): 
    global event1,event2
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            clickButton = i
            event2.set()  
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(fontStyle,16)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)



def Esc(msg,x,y,w,h,ic,ac,action=None): 
    global event2
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            pygame.quit()
            os.system("sudo python Owl-GUI.py")
  
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(fontStyle,20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def Back(msg,x,y,w,h,ic,ac,action=None): 
    global event2
    global clickButton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            pygame.quit()
            #os.system("sudo python Pupil-wifi.py")
  
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(fontStyle,20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def Connect(msg,x,y,w,h,ic,ac,action=None): 
    global event3
    pygame.font.init()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            event3.set()
            upd1() 
            print("event is set") 
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font(None,20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

# to create textobjects	
def text_objects(text,font):
    textSurface = font.render(text, True,black)
    return textSurface,textSurface.get_rect()


if __name__ == '__main__':
    os.system('sudo pkill -9 -f Owl-GUI.py')
    pygame.init()
    upd(event1,event2,event3)
    #p4 = Process(target=upd, args=(event1,event2,event3,))# to update the display
    #p4.start()   
    #p4.join()   


