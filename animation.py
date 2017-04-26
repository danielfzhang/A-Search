#!/usr/bin/python3
from Asearch import Astar
import pygame
import math
from pygame.locals import *
from sys import exit
import time
#searching parameters
zoomin=6
win_size=120
start=[10,10]
end=[100,100]
blocks=[]
step_cost=1
delay=0.01
#color definition
WHITE=[255,255,255]
RED=[255,0,0]
BLACK=[0,0,0]
BLUE=[141,182,205]
GREEN=[0,255,127]
#pygame initialization
pygame.init()
screen = pygame.display.set_mode((win_size*zoomin, win_size*zoomin), 0, 32)
screen.fill(WHITE)
pygame.draw.rect(screen, RED, (start[0]*zoomin, start[1]*zoomin,zoomin,zoomin))
pygame.draw.rect(screen, RED, (end[0]*zoomin, end[1]*zoomin,zoomin,zoomin))
pygame.display.set_caption("Find a path")
pygame.display.update()
#flags
buttondown=False
search=False
DoSearch=False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif not DoSearch:
            if event.type ==  MOUSEBUTTONDOWN and not DoSearch:
                buttondown=True
            elif event.type ==  MOUSEBUTTONUP and not DoSearch:
                buttondown=False
            elif event.type == KEYDOWN and not DoSearch:
                if event.key == K_RETURN:
                    search=True
    if not DoSearch:
        if search:
            Asearch=Astar(start,end,blocks,win_size,step_cost)
            while True:
                result=Asearch.oneSearch()
                if result!="find path" and result!="no path":
                    cir_x=math.ceil(result[0]*zoomin+zoomin/2-1)
                    cir_y=math.ceil(result[1]*zoomin+zoomin/2-1)
                    pygame.draw.circle(screen, BLUE, (cir_x, cir_y), math.ceil(zoomin/2))
                    pygame.display.update()
                    time.sleep(delay)
                else:
                    DoSearch=True
                    for p in Asearch.shortestPath:
                        cir_x=math.ceil(p[0]*zoomin+zoomin/2-1)
                        cir_y=math.ceil(p[1]*zoomin+zoomin/2-1)
                        pygame.draw.circle(screen, GREEN, (cir_x, cir_y),math.ceil(zoomin/2))
                        pygame.display.update()
                        time.sleep(delay/2)
                    break
        elif buttondown:
            x, y = pygame.mouse.get_pos()
            x=math.ceil(x/zoomin)
            y=math.ceil(y/zoomin)
            if [x,y] not in blocks:
                blocks.append([x,y])
            pygame.draw.rect(screen, BLACK, (x*zoomin, y*zoomin,zoomin,zoomin))
            pygame.display.update()
