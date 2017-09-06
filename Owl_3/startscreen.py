
#!/usr/bin/python

import pygame
import time
import random
import pygame.camera
import os
import sys
from multiprocessing import Process, Queue, Event
from PIL import Image
from datetime import datetime
import datetime

from pygame.locals import *


datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

time_stamp = datetime.datetime.now().strftime("%Y_%m_%d")

display_width = 800
display_height = 480

width=100
height=50

black = (0,0,0)
white= (255,255,255)


chocolate=(210,105,30)
khaki=(240,230,140)
olive=(128,128,0)

size=(800,480)
screen = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
pygame.display.set_caption('OWL')
clock = pygame.time.Clock()
text=""


plot = pygame.image.load('/home/pi/openDR/startscreen.jpg')
plot_resized = pygame.transform.scale(plot,size)

def loop():
    pygame.init()
    font = pygame.font.Font(None, height)
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
	#screen.fill(white)
        screen.blit(plot_resized,(0,0))
        button("Next",0,0,display_width,display_height,olive,chocolate)
        pygame.display.flip()
	
def text_objects(text,font):
    textSurface = font.render(text, True,white)
    return textSurface,textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):  
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
       # print("clicked")
       # pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            #execute = ("python Pupil-Timestamp.py")
            pygame.quit()
            execute = ("sudo python /home/pi/openDR/Owl-GUI.py")
            os.system(execute)
            #pygame.quit()   

       
if __name__ == "__main__":  
    pygame.init()        
    loop()
