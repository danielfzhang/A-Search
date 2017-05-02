#!/usr/bin/python3
from helper import *
from pygame.locals import *
from sys import exit
import pygame, os, threading, random
#parameters
MBsize=78
miniMapSize=3
windowSize=(1300, MBsize*11)
moveSpeed=0
Shifting=[30,0]
Grey=[105,105,105]
#colors
White=[255,255,255]
Black=[0,0,0]
Red=[255,0,0]
Green=[0,255,0]
#window set up
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
pygame.init()
screen = pygame.display.set_mode(windowSize, 0, 32)
pygame.display.set_caption("Maze Defense")
#load, and analyze images
mazeSize,Start,End,blockList=analyzeMaze('img/maze1.PNG')
Monster=pygame.image.load('img/monster.PNG').convert_alpha()
Monster = pygame.transform.scale(Monster, (MBsize, MBsize))
monsterPos=End[:]
#functions-----------
def updateMap():#draw Map
    screen.fill(White)
    for x in range(-5,6):
        for y in range(-5,6):
            if [monsterPos[0]+x,monsterPos[1]+y] in blockList:
                pygame.draw.rect(screen,Black,[(x+5)*MBsize+Shifting[0],(y+5)*MBsize+Shifting[1],MBsize,MBsize])
    else: screen.blit(Monster, [5*MBsize+Shifting[0],5*MBsize+Shifting[1]])
    #draw minimap
    pygame.draw.rect(screen,White,Shifting+[mazeSize[0]*miniMapSize,mazeSize[1]*miniMapSize])
    for pixel in blockList:
        pygame.draw.rect(screen,Grey,[p[0]*miniMapSize+p[1] for p in zip(pixel,Shifting)]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Green,[p[0]*miniMapSize+p[1] for p in zip(End,Shifting)]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Green,[p[0]*miniMapSize+p[1] for p in zip(Start,Shifting)]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Red,[p[0]*miniMapSize+p[1] for p in zip(monsterPos,Shifting)]+[miniMapSize,miniMapSize])
    pygame.display.update()
updateMap()
def toDestn(destination):#move to destination
    global autoMove, monsterPos
    while monsterPos!=destination:
        if not autoMove: return#interrupted
        Asearch=Astar(monsterPos,destination,blockList,mazeSize)
        result=Asearch.oneSearch()
        while result!="find path" and result!="no path":
            result=Asearch.oneSearch()
        if result=="find path":
            if len(Asearch.shortestPath)>1:
                if not autoMove: return#interrupted
                monsterPos=Asearch.shortestPath[1]
                pygame.time.delay(moveSpeed)
    autoMove=False
#flags
drawBLK=False
drawWHT=False
autoMove=False
left=right=up=down=False
#pygame main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT: exit()
        elif event.type ==  MOUSEBUTTONDOWN:
            pressed_mouse = pygame.mouse.get_pressed()
            if pressed_mouse[0]: drawBLK=True#left click to set blocks
            elif pressed_mouse[2]: drawWHT=True#right click to remove blocks
        elif event.type ==  MOUSEBUTTONUP:
            drawBLK=False
            drawWHT=False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN and not autoMove:#automatically walk to destination
                autoMove=True
                t1=threading.Thread(target=toDestn,args=(Start,))
                t1.setDaemon(True)
                t1.start()
            else:
                autoMove=False
                #control monster by up, down, right, left arrow keys
                if event.key == K_UP:
                    if [monsterPos[0],monsterPos[1]-1] not in blockList:
                        monsterPos[1]-=1
                elif event.key == K_DOWN:
                    if [monsterPos[0],monsterPos[1]+1] not in blockList:
                        monsterPos[1]+=1
                elif event.key == K_RIGHT:
                    if [monsterPos[0]+1,monsterPos[1]] not in blockList:
                        if monsterPos[0]+1<mazeSize[0]: monsterPos[0]+=1
                elif event.key == K_LEFT:
                    if [monsterPos[0]-1,monsterPos[1]] not in blockList:
                        if monsterPos[0]>0: monsterPos[0]-=1
    if drawBLK:#left click set blocks
        x, y = pygame.mouse.get_pos()
        x=(x-Shifting[0])//MBsize-5+monsterPos[0]
        y=(y-Shifting[1])//MBsize-5+monsterPos[1]
        if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
            if [x,y] not in blockList: blockList.append([x,y])
    elif drawWHT:#right click remove blocks
        x, y = pygame.mouse.get_pos()
        x=(x-Shifting[0])//MBsize-5+monsterPos[0]
        y=(y-Shifting[1])//MBsize-5+monsterPos[1]
        if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
            if [x,y] in blockList: blockList.remove([x,y])
    updateMap()
