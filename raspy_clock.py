#!/home/pi/miniconda3/bin/python
from itertools import cycle
import random
import sys
import math

import pygame
from pygame.locals import *
import datetime


FPS = 4
SCREENWIDTH  = 800
SCREENHEIGHT = 480
IMAGES={}
try:
    xrange
except NameError:
    xrange = range

class debug_clock():
    def __init__(self):
        self.hour=8
        self.minute=0
        self.second=0
    def ticktock(self):
        self.minute+=10
        if self.minute>59:
            self.minute=self.minute%60
            self.hour+=1
        if self.hour>23:
            self.hour=self.hour%24


def main(debug=0):
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),pygame.FULLSCREEN)
    # SCREEN = pygame.display.set_mode(pygame.FULLSCREEN)
    pygame.display.set_caption('Raspy-clock')

    IMAGES['background']=pygame.image.load('assets/background_800x480.jpg')
    IMAGES['day_background']=pygame.image.load('assets/day_background.jpg')
    IMAGES['night_background']=pygame.image.load('assets/night_background.jpg')
    IMAGES['mountain']=pygame.image.load('assets/mountain_bright.png').convert_alpha()
    IMAGES['sun']=pygame.image.load('assets/sun.png').convert_alpha()
    IMAGES['moon']=pygame.image.load('assets/moon.png').convert_alpha()

    IMAGES['colon']=pygame.image.load('digits/colon.png').convert_alpha()
    IMAGES['null']=pygame.image.load('digits/null.png').convert_alpha()
    IMAGES['numbers'] = (
        pygame.image.load('digits/0.png').convert_alpha(),
        pygame.image.load('digits/1.png').convert_alpha(),
        pygame.image.load('digits/2.png').convert_alpha(),
        pygame.image.load('digits/3.png').convert_alpha(),
        pygame.image.load('digits/4.png').convert_alpha(),
        pygame.image.load('digits/5.png').convert_alpha(),
        pygame.image.load('digits/6.png').convert_alpha(),
        pygame.image.load('digits/7.png').convert_alpha(),
        pygame.image.load('digits/8.png').convert_alpha(),
        pygame.image.load('digits/9.png').convert_alpha()
    )

    showClock(debug)


def night_sky_alpha(now):
    if now.hour in [22,23,0,1,2,3]:
        return 255
    if now.hour in [8,9,10,11,12,13,14,15,16,17]:
        return 0
    total_minutes=now.hour*60+now.minute
    if total_minutes<=480: # 4am -8am fade out
        return int(255-255*(total_minutes-240)/240)
    if total_minutes>=1080: #6pm-10pm fade in
        return int(255*(total_minutes-1080)/240)

def show_sun(now):
    total_minutes=now.hour*60+now.minute
    start_time=6*60
    end_time=18*60
    x=(total_minutes-start_time)/(end_time-start_time)
    y=x*x-x+0.65
    SCREEN.blit(IMAGES['sun'], (int(x*800),int(y*480)))

def show_moon(now):
    total_minutes=now.hour*60+now.minute
    start_time=19*60
    end_time=24*60+6*60
    if total_minutes<=start_time:
        total_minutes=total_minutes+24*60
    x=(total_minutes-start_time)/(end_time-start_time)
    y=x*x-x+0.65
    SCREEN.blit(IMAGES['moon'], (int(x*800),int(y*480)))


def night_moutain(now,last_darkness):
    """Fill all pixels of the surface with color, preserve transparency."""
    if now.hour in [22,23,0,1,2,3]:
        darkness=0.2
    if now.hour in [10,11,12,13,14,15]:
        darkness=0.9
    total_minutes=now.hour*60+now.minute
    if total_minutes<=600 and total_minutes>=240: # 4am -10 am increase darkness
        darkness=0.2+0.7*(total_minutes-240)/360
    if total_minutes>=960 and total_minutes<=1320: #4pm -10pm decrease darkness
        darkness=0.9-0.7*(total_minutes-960)/360

    if abs(darkness-last_darkness[0])>0.1:
        last_darkness[0]=darkness
        IMAGES['mountain_copy']=IMAGES['mountain'].copy()
        w, h =IMAGES['mountain_copy'].get_size()
        for x in range(w):
            for y in range(h):
                color = IMAGES['mountain_copy'].get_at((x, y))
                IMAGES['mountain_copy'].set_at((x, y), Color(int(color[0]*darkness),int(color[1]*darkness),int(color[2]*darkness),color[3]))
    SCREEN.blit(IMAGES['mountain_copy'], (0,480-191))


def showClock(debug=0):
    """Shows clock on screen"""
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0
    last_darkness=[-1]
    now=debug_clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        if debug:
            now.ticktock()
        else:
            now = datetime.datetime.now()

        # draw sprites
        SCREEN.blit(IMAGES['day_background'], (0,0))
        IMAGES['night_background'].set_alpha(night_sky_alpha(now))
        SCREEN.blit(IMAGES['night_background'], (0,0))

        show_sun(now)
        show_moon(now)
    
        night_moutain(now,last_darkness)
        
        showNumbers_Hr(now.hour)
        showNumbers_Mm(now.minute)
        if loopIter>=4:
            showColon()
        else:
            showNull()
        pygame.display.update()
        loopIter = (loopIter+1)%8
        FPSCLOCK.tick(FPS)


def showNumbers_Hr(number):
    """displays number center of screen"""
    numberDigits = [int(x) for x in list(str(number))]
    if len(numberDigits)==1:
    	numberDigits=[0]+numberDigits
    totalWidth = 0 # total width of all numbers to be printed

    for digit in numberDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH/2 - totalWidth) / 2

    for digit in numberDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()*0.7

def showNumbers_Mm(number):
    """displays number center of screen"""
    numberDigits = [int(x) for x in list(str(number))]
    if len(numberDigits)==1:
    	numberDigits=[0]+numberDigits
    totalWidth = 0 # total width of all numbers to be printed

    for digit in numberDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH/2 - totalWidth) / 2+SCREENWIDTH/1.8 

    for digit in numberDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()*0.7

def showColon():
	totalWidth = IMAGES['colon'].get_width()
	Xoffset = (SCREENWIDTH - totalWidth) / 2
	SCREEN.blit(IMAGES['colon'], (Xoffset, SCREENHEIGHT * 0.1))

def showNull():
	totalWidth = IMAGES['null'].get_width()
	Xoffset = (SCREENWIDTH - totalWidth) / 2
	SCREEN.blit(IMAGES['null'], (Xoffset, SCREENHEIGHT * 0.1))


if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]:
        debug=1
        print("now in debug mode!")
    else:
        debug=0
    main(debug)
