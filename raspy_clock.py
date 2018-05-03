from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *
import datetime


FPS = 30
SCREENWIDTH  = 800
SCREENHEIGHT = 480
IMAGES={}
try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Raspy-clock')

    IMAGES['background']=pygame.image.load('background_800x480.jpg')
    # numbers sprites for score display

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

    showClock()


def showClock():
    """Shows clock on screen"""
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        now = datetime.datetime.now()

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        showNumbers_Hr(now.hour)
        showNumbers_Mm(now.minute)
        if loopIter>=30:
            showColon()
        else:
            showNull()
        pygame.display.update()
        loopIter = (loopIter+1)%60
        FPSCLOCK.tick(FPS)


def showNumbers_Hr(number):
    """displays number center of screen"""
    numberDigits = [int(x) for x in list(str(number))]
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
    main()
