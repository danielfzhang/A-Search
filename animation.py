#!/usr/bin/python3
from Asearch import Astar
import pygame
import math
from pygame.locals import *
from sys import exit

#searching parameters
zoomin=5
win_size=120
start=[1,1]
end=[100,100]
blocks=[]
step_cost=1
#color definition
WHITE=[255,255,255]
BROWN=[238,59,59]
RED=[255,0,0]
BLACK=[0,0,0]
SEAGREEN=[32,178,170]
#pygame initialization
pygame.init()
screen = pygame.display.set_mode((win_size*zoomin, win_size*zoomin), 0, 32)
screen.fill(WHITE)
pygame.draw.rect(screen,BLACK, (start[0]*zoomin, start[1]*zoomin,zoomin,zoomin))
pygame.draw.rect(screen,BLACK, (end[0]*zoomin, end[1]*zoomin,zoomin,zoomin))
pygame.display.set_caption("Find a path")
buttondown=False
search=False
done=False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type ==  MOUSEBUTTONDOWN and not done:
            buttondown=True
        elif event.type ==  MOUSEBUTTONUP and not done:
            buttondown=False
        elif event.type == KEYDOWN and not done:
            if event.key == K_RETURN:
                search=True
    if search:
        Asearch=Astar(start,end,blocks,win_size,step_cost)
        while True:
            result=Asearch.oneSearch()
            if result!="find path" and result!="openlist empty":
                pygame.draw.rect(screen, BROWN, (result[0]*zoomin, result[1]*zoomin,zoomin,zoomin))
                pygame.display.update()
            else:
                done=True
                break
    elif buttondown:
        x, y = pygame.mouse.get_pos()
        x=math.ceil(x/5)
        y=math.ceil(y/5)
        if [x,y] not in blocks:
            blocks.append([x,y])
        pygame.draw.rect(screen, SEAGREEN, (x*zoomin, y*zoomin,zoomin,zoomin))

    pygame.display.update()
