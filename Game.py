#!/usr/bin/python3
from helper import *
from pygame.locals import *
from sys import exit
import pygame, os, threading, random, math
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
#colors
Grey=[105,105,105]
White=[255,255,255]
Black=[0,0,0]
Red=[255,0,0]
Green=[0,255,0]
#load,analyze images
Shifting=[0,0]
MBsize=60
MBnum=[24,14]
miniMapSize=5
monsterSpeed=100
windowSize=(Shifting[0]+MBsize*MBnum[0], MBsize*MBnum[1])
pygame.init()
screen = pygame.display.set_mode(windowSize, 0, 32)
filename=random.randint(1, 4)
filename='img/maze' + str(filename)+'.PNG'
mazeSize,Start,End,blockList=analyzeMaze(filename)
#window set up
monsterPos=[-1,-1]
viewPoint=[Shifting[0]+MBnum[0]//2,mazeSize[1]//2]
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Defense")
Monster=pygame.image.load('img/monster.PNG').convert_alpha()
Monster = pygame.transform.scale(Monster, (MBsize, MBsize))
Stone=pygame.image.load('img/stone.PNG')
Stone= pygame.transform.scale(Stone, (MBsize, MBsize))
Land=pygame.image.load('img/land.PNG')
Land= pygame.transform.scale(Land, (MBsize, MBsize))
#(functions-----------
def updateMap():
    global viewPoint
    screen.fill(White)
    for x in range(MBnum[0]//2*-1,MBnum[0]//2):#draw rows
        for y in range(MBnum[1]//2*-1,MBnum[1]//2):#draw cols
            if 0<=viewPoint[0]+x<mazeSize[0] and 0<=viewPoint[1]+y<mazeSize[1]:
                if [viewPoint[0]+x,viewPoint[1]+y] in blockList:
                    screen.blit(Stone, [(x+MBnum[0]//2)*MBsize+Shifting[0],(y+MBnum[1]//2)*MBsize+Shifting[1]])
                else: screen.blit(Land, [(x+MBnum[0]//2)*MBsize+Shifting[0],(y+MBnum[1]//2)*MBsize+Shifting[1]])
                if [viewPoint[0]+x,viewPoint[1]+y]==monsterPos:#draw monster
                    if monsterPos!=[-1,-1]:
                        screen.blit(Monster, [(x+MBnum[0]//2)*MBsize+Shifting[0],(y+MBnum[1]//2)*MBsize+Shifting[1]])
    #draw minimap
    pygame.draw.rect(screen,White,Shifting+[mazeSize[0]*miniMapSize,mazeSize[1]*miniMapSize])
    for pixel in blockList:
        pygame.draw.rect(screen,Grey,[p[0]*miniMapSize+p[1] for p in zip(pixel,Shifting)]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Green,[p[0]*miniMapSize+p[1] for p in zip(End,Shifting)]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Green,[p[0]*miniMapSize+p[1] for p in zip(Start,Shifting)]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Red,[p[0]*miniMapSize+p[1] for p in zip(monsterPos,Shifting)]+[miniMapSize,miniMapSize])
    miniWin=[viewPoint[0]-MBnum[0]//2,viewPoint[1]-MBnum[1]//2]
    pygame.draw.rect(screen,Red,[p[0]*miniMapSize+p[1] for p in zip(miniWin,Shifting)]+[MBnum[0]*miniMapSize,MBnum[1]*miniMapSize],2)
    pygame.display.flip()
    clock.tick(30)
def geneMonster(destination):
    global monsterPos, monsterMove
    monsterPos=End[:]
    preStep=[[],[]]#track last two steps
    while monsterMove:
        Asearch=Astar(monsterPos,destination,blockList,mazeSize)
        nextStp=Asearch.nextStep()
        deadlck=preStep.pop(0)
        if deadlck==nextStp:#detect dead lock
            randmove=[]
            direct4=[[0,-1],[0,1],[-1,0],[1,0]]#up,down,left,right
            #add available points to randmove
            for direction in direct4:
                point_x=monsterPos[0]+direction[0]
                point_y=monsterPos[1]+direction[1]
                #the point is within the window
                if 0<=point_x<mazeSize[0] and 0<=point_y<mazeSize[1]:
                    point=[point_x,point_y]
                    if point not in blockList and point!=deadlck:
                        randmove.append(point)
            nextStp=random.choice(randmove)
            preStep=[[],[]]
            pygame.time.delay(monsterSpeed*3)
        else: preStep.append(nextStp)

        if nextStp==None: pass
        else:
            monsterPos=nextStp#move
            pygame.time.delay(monsterSpeed)
            if nextStp==destination:
                monsterPos=[-1,-1]
                monsterMove=False#reach destination
#-------------functions)
updateMap()
#flags
monsterMove=False
leftClick=False
rightClick=False
#pygame main loop
while True:
    for event in pygame.event.get():#detect keyboard, mouse inputs
        if event.type == QUIT: exit()
    #(mouse functions-----
    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0] or pressed_mouse[2]:
        x, y = pygame.mouse.get_pos()
        #click minimap to move map
        if Shifting[0]<=x<Shifting[0]+miniMapSize*mazeSize[0] and Shifting[1]<=y<Shifting[1]+miniMapSize*mazeSize[1]:
            if pressed_mouse[0]:
                if x<Shifting[0]+MBnum[0]//2*miniMapSize:
                    x=Shifting[0]+MBnum[0]//2
                elif x>=Shifting[0]+(mazeSize[0]-MBnum[0]//2)*miniMapSize:
                    x=Shifting[0]+mazeSize[0]-MBnum[0]//2
                else:
                    x=(x-Shifting[0])//miniMapSize

                if y<Shifting[1]+MBnum[1]//2*miniMapSize:
                    y=Shifting[1]+MBnum[1]//2
                elif y>=Shifting[1]+(mazeSize[1]-MBnum[1]//2)*miniMapSize:
                    y=Shifting[1]+mazeSize[1]-MBnum[1]//2
                else:
                    y=(y-Shifting[1])//miniMapSize
                viewPoint=[x,y]
        else:
            if pressed_mouse[0]:#click left mouse button to set block
                x=(x-Shifting[0])//MBsize-MBnum[0]//2+viewPoint[0]
                y=(y-Shifting[1])//MBsize-MBnum[1]//2+viewPoint[1]
                if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
                    if [x,y] not in blockList: blockList.append([x,y])
            else:#click right mouse button to remove block
                x, y = pygame.mouse.get_pos()
                x=(x-Shifting[0])//MBsize-MBnum[0]//2+viewPoint[0]
                y=(y-Shifting[1])//MBsize-MBnum[1]//2+viewPoint[1]
                if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
                    if [x,y] in blockList: blockList.remove([x,y])
    #----------)
    #(keyboard functions-----
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_RETURN] and not monsterMove:#generage monster
        monsterMove=True
        t1=threading.Thread(target=geneMonster,args=(Start,))
        t1.setDaemon(True)
        t1.start()
    #move view point
    elif pressed_key[pygame.K_UP]:
        if viewPoint[1]>Shifting[1]: viewPoint[1]-=1
    elif pressed_key[pygame.K_DOWN]:
        if viewPoint[1]<Shifting[1]+mazeSize[1]: viewPoint[1]+=1
    elif pressed_key[pygame.K_RIGHT]:
        if viewPoint[0]<Shifting[0]+mazeSize[0]: viewPoint[0]+=1
    elif pressed_key[pygame.K_LEFT]:
        if viewPoint[0]>Shifting[0]: viewPoint[0]-=1
    #------------)
    updateMap()
