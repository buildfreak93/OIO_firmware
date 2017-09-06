#!/usr/bin/python

import pygame
import time
from time import gmtime,strftime
import random
import os
import sys

pygame.init()
pygame.font.init()
pygame.display.init()
#showtime = strftime("%Y-%M-%D %H:%M:%S",gmtime())
showtime = strftime("%Y-%M-%D",gmtime())
from pygame.locals import *
file=open('/home/pi/openDR/mr.txt')
mr_num=file.readline()
file.close()

file=open('/home/pi/openDR/grade.txt')
gradeVal=file.readline()
file.close()

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
screen.fill(black)
pygame.display.set_caption('OWL')
clock = pygame.time.Clock()

next_Btn=pygame.image.load('/home/pi/openDR/next.png')
logo=pygame.image.load('/home/pi/openDR/owlLogo.jpg')
logo_resized=pygame.transform.scale(logo,(200,100))

screen.blit(logo_resized,(300,30))
screen.blit(next_Btn,(750,185))

def name():
    pygame.init()
    font = pygame.font.SysFont(fontStyle, fontSize)
    font1 = pygame.font.SysFont(fontStyle, 20)
    running = True
    while running:
        pygame.display.flip()
        for event in pygame.event.get():           
            if event.type == QUIT:
                pygame.quit()
                running = False  
        main_text = font.render('Patient Details :',0,(255,255,255))
        mrnum_text = font.render('MR_Number :',0,(255,255,255))
        grade_text = font.render('Grade :',0,(255,255,255))
        time_text = font.render('Time :',0,(255,255,255))

        main_text = font.render('Patient Details :',0,(255,255,255))
        mrnum_val = font.render(mr_num,0,(255,255,255))
        grade_val = font.render(gradeVal,0,(255,255,255))
        time_val = font.render(showtime,0,(255,255,255))

        screen.blit(main_text,(210,150))
        screen.blit(mrnum_text,(210,180))
        screen.blit(grade_text,(210,210))
        screen.blit(time_text,(210,240))

        screen.blit(mrnum_val,(410,180))
        screen.blit(grade_val,(410,210))
        screen.blit(time_val,(410,240))

        button(msg_2,750,176,21,48,olive,chocolate)
        pygame.display.flip()
        #button1(msg_1,750,30,30,30,olive,chocolate)
        #button2("Next",25,30,30,22,olive,chocolate)


def text_objects(text,font):
    textSurface = font.render(text, True,black)
    return textSurface,textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None): 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action ==None:
            print("success")
            pygame.quit()
            execute = ("sudo python /home/pi/openDR/Owl-GUI.py")
            os.system(execute)  
   # else:
        #pygame.draw.rect(screen, ic,(x,y,w,h))

   # smallText = pygame.font.SysFont(fontStyle,fontSize)
   # textSurf, textRect = text_objects(msg, smallText)
   # textRect.center = ( (x+(w/2)), (y+(h/2)) )
   # screen.blit(textSurf, textRect)

if __name__ == "__main__":
    os.system("sudo pkill -9 -f fundus_v4.py")
    name()