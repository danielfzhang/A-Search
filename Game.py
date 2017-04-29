#!/usr/bin/python3
from helper import *
from pygame.locals import *
from sys import exit
import pygame, math, os
#parameter definition
WHITE=[255,255,255]
RED=[255,0,0]
BLACK=[0,0,0]
BLUE=[141,182,205]
CADETBLUE=[152,245,255]
Enlarge=28
#analyze maze
file= input("enter the file name of maze in folder maze:")
file="maze/"+file
MazeSize,Start,End,BlockList=analyzeMaze(file)
#set the position of screen as (0,30)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
#pygame initialization
pygame.init()
screen = pygame.display.set_mode((MazeSize[0]*Enlarge, MazeSize[1]*Enlarge), 0, 32)
pygame.display.set_caption("Maze Defense")
#draw Maze
def drawMaze():
    screen.fill(WHITE)
    for pixel in BlockList:
        pygame.draw.rect(screen,BLACK,[pixel[0]*Enlarge,pixel[1]*Enlarge,Enlarge,Enlarge])
    pygame.draw.rect(screen,BLUE,[End[0]*Enlarge,End[1]*Enlarge,Enlarge,Enlarge])
    pygame.draw.rect(screen,RED,[Start[0]*Enlarge,Start[1]*Enlarge,Enlarge,Enlarge])
    pygame.display.update()
drawMaze()
#flags
buttonDown=False
showPath=False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type ==  MOUSEBUTTONDOWN:
            buttonDown=True
        elif event.type ==  MOUSEBUTTONUP:
            buttonDown=False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                Asearch=Astar(Start,End,BlockList,MazeSize)
                result=Asearch.oneSearch()
                while result!="find path" and result!="no path":
                    result=Asearch.oneSearch()
                for p in Asearch.shortestPath:
                    cir_x=math.floor(p[0]*Enlarge+Enlarge/2-1)
                    cir_y=math.floor(p[1]*Enlarge+Enlarge/2-1)
                    pygame.draw.circle(screen, CADETBLUE, (cir_x, cir_y),math.floor(Enlarge/2))
                    pygame.display.update()
            elif event.key == K_UP:
                if [Start[0],Start[1]-1] not in BlockList:
                    Start[1]-=1
                    drawMaze()
            elif event.key == K_DOWN:
                if [Start[0],Start[1]+1] not in BlockList:
                    Start[1]+=1
                    drawMaze()
            elif event.key == K_RIGHT:
                if [Start[0]+1,Start[1]] not in BlockList:
                    Start[0]+=1
                    drawMaze()
            elif event.key == K_LEFT:
                if [Start[0]-1,Start[1]] not in BlockList:
                    Start[0]-=1
                    drawMaze()

    if buttonDown:
        x, y = pygame.mouse.get_pos()
        x=math.floor(x/Enlarge)
        y=math.floor(y/Enlarge)
        if [x,y] not in BlockList:
            BlockList.append([x,y])
        pygame.draw.rect(screen, BLACK, (x*Enlarge, y*Enlarge,Enlarge,Enlarge))
        pygame.display.update()
