#!/usr/bin/python3
from astar import Astar
from analyzemaze import *
import pygame
import math
from pygame.locals import *
from sys import exit
#parameter definition
WHITE=[255,255,255]
RED=[255,0,0]
BLACK=[0,0,0]
BLUE=[141,182,205]
Enlarge=4
#analyze maze
file= input("enter the file name of maze in folder maze:")
file="maze/"+file
MazeSize,Start,End,BlockList=analyzeMaze(file)
#pygame initialization
pygame.init()
screen = pygame.display.set_mode((MazeSize[0]*Enlarge, MazeSize[1]*Enlarge), 0, 32)
screen.fill(WHITE)
pygame.display.set_caption("Maze")
#draw blocks, start point and end point
for pixel in BlockList:
    pygame.draw.rect(screen,BLACK,[pixel[0]*Enlarge,pixel[1]*Enlarge,Enlarge,Enlarge])
pygame.draw.rect(screen,RED,[Start[0]*Enlarge,Start[1]*Enlarge,Enlarge,Enlarge])
pygame.draw.rect(screen,RED,[End[0]*Enlarge,End[1]*Enlarge,Enlarge,Enlarge])
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
            Asearch=Astar(Start,End,BlockList,MazeSize)
            while True:
                result=Asearch.oneSearch()
                if result!="find path" and result!="no path":
                    cir_x=math.floor(result[0]*Enlarge+Enlarge/2-1)
                    cir_y=math.floor(result[1]*Enlarge+Enlarge/2-1)
                    pygame.draw.circle(screen, BLUE, (cir_x, cir_y), math.floor(Enlarge/2))
                    pygame.display.update()
                else:
                    DoSearch=True
                    for p in Asearch.shortestPath:
                        cir_x=math.floor(p[0]*Enlarge+Enlarge/2-1)
                        cir_y=math.floor(p[1]*Enlarge+Enlarge/2-1)
                        pygame.draw.circle(screen, RED, (cir_x, cir_y),math.floor(Enlarge/2))
                        pygame.display.update()
                    break
        elif buttondown:
            x, y = pygame.mouse.get_pos()
            x=math.floor(x/Enlarge)
            y=math.floor(y/Enlarge)
            if [x,y] not in BlockList:
                BlockList.append([x,y])
            pygame.draw.rect(screen, BLACK, (x*Enlarge, y*Enlarge,Enlarge,Enlarge))
            pygame.display.update()
