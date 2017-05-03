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
#parameters set up
MBsize=70
MBnum=[24,14]
miniMapSize=4
bagOpen=False
bagSize=[MBsize*2,MBsize*3]
bagPos=[MBsize*(MBnum[0]//2)-bagSize[0]//2, MBsize*(MBnum[1]//2)-bagSize[1]//2]
#load,analyze images
monsterSpeed=100
windowSize=(MBsize*MBnum[0], MBsize*MBnum[1])
pygame.init()
font = pygame.font.SysFont(None, MBsize//2)
screen = pygame.display.set_mode(windowSize, 0, 32)
filename=random.randint(1, 4)
filename='img/maze' + str(filename)+'.PNG'
mazeSize,Start,End,blockList=analyzeMaze(filename)
#window set up
cavePos=random.choice(blockList)
while cavePos[0]==0 or cavePos[1]==0 or cavePos[0]==mazeSize[0]-1 or cavePos[1]==mazeSize[1]-1:
    cavePos=random.choice(blockList)
monsterPos=[-1,-1]
viewPoint=[+MBnum[0]//2,mazeSize[1]//2]
clock = pygame.time.Clock()
pygame.display.set_caption("Maze Defense")
Monster=pygame.image.load('img/monster.PNG').convert_alpha()
Monster = pygame.transform.scale(Monster, (MBsize, MBsize))
Wall=pygame.image.load('img/wall.PNG')
Wall= pygame.transform.scale(Wall, (MBsize, MBsize))
Land=pygame.image.load('img/land.PNG')
Land= pygame.transform.scale(Land, (MBsize, MBsize))
Chest=pygame.image.load('img/chest.PNG')
Chest= pygame.transform.scale(Chest, (MBsize, MBsize))
Archer=pygame.image.load('img/archer.PNG')
Archer= pygame.transform.scale(Archer, (MBsize, MBsize))
Shovel=pygame.image.load('img/shovel.PNG')
Shovel=pygame.transform.scale(Shovel, (MBsize, MBsize))
Brick=pygame.image.load('img/brick.PNG')
Brick=pygame.transform.scale(Brick, (MBsize, MBsize))
archerNum=1
shovelNum=1
brickNum=1
#(functions-----------
def updateMap():
    global viewPoint
    screen.fill(White)
    for x in range(MBnum[0]//2*-1,MBnum[0]//2):#draw rows
        for y in range(MBnum[1]//2*-1,MBnum[1]//2):#draw cols
            if 0<=viewPoint[0]+x<mazeSize[0] and 0<=viewPoint[1]+y<mazeSize[1]:
                if [viewPoint[0]+x,viewPoint[1]+y] in blockList:
                    screen.blit(Wall, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                else:
                    screen.blit(Land, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                    if [viewPoint[0]+x,viewPoint[1]+y]==cavePos:
                        screen.blit(Cave, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                if [viewPoint[0]+x,viewPoint[1]+y]==monsterPos:#draw monster
                    if monsterPos!=[-1,-1]:
                        screen.blit(Monster, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
    #draw minimap
    pygame.draw.rect(screen,White,[0,0,mazeSize[0]*miniMapSize,mazeSize[1]*miniMapSize])
    for pixel in blockList:
        pygame.draw.rect(screen,Grey,[p[0]*miniMapSize+p[1] for p in zip(pixel,[0,0])]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Green,[p[0]*miniMapSize+p[1] for p in zip(End,[0,0])]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Green,[p[0]*miniMapSize+p[1] for p in zip(Start,[0,0])]+[miniMapSize,miniMapSize])
    pygame.draw.rect(screen,Red,[p[0]*miniMapSize+p[1] for p in zip(monsterPos,[0,0])]+[miniMapSize,miniMapSize])
    miniWin=[viewPoint[0]-MBnum[0]//2,viewPoint[1]-MBnum[1]//2]
    pygame.draw.rect(screen,Red,[p[0]*miniMapSize+p[1] for p in zip(miniWin,[0,0])]+[MBnum[0]*miniMapSize,MBnum[1]*miniMapSize],2)
    #bag
    if bagOpen:
        archerItem = font.render("X"+str(archerNum), True, Black)
        shovelItem = font.render("X"+str(shovelNum), True, Black)
        brickItem = font.render("X"+str(brickNum), True, Black)
        pygame.draw.rect(screen,White,bagPos+bagSize)
        screen.blit(Archer, bagPos)
        screen.blit(archerItem, [bagPos[0]+MBsize,bagPos[1]+MBsize//4])
        screen.blit(Shovel, [bagPos[0],bagPos[1]+MBsize])
        screen.blit(shovelItem, [bagPos[0]+MBsize,bagPos[1]+MBsize//4])
        screen.blit(Brick, [bagPos[0],bagPos[1]+MBsize*2])
        screen.blit(brickItem, [bagPos[0]+MBsize,bagPos[1]+MBsize*2+MBsize//4])
    pygame.display.flip()
    clock.tick(60)
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
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_d and not bagOpen:
                bagOpen=True
            elif event.key == K_d and bagOpen:
                bagOpen=False

    #(mouse functions-----
    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0] or pressed_mouse[2]:
        x, y = pygame.mouse.get_pos()
        #click minimap to move map
        if 0<=x<miniMapSize*mazeSize[0] and 0<=y<miniMapSize*mazeSize[1]:
            if pressed_mouse[0]:
                if x<MBnum[0]//2*miniMapSize:
                    x=MBnum[0]//2
                elif x>=(mazeSize[0]-MBnum[0]//2)*miniMapSize:
                    x=mazeSize[0]-MBnum[0]//2
                else:
                    x=(x)//miniMapSize

                if y<MBnum[1]//2*miniMapSize:
                    y=MBnum[1]//2
                elif y>=+(mazeSize[1]-MBnum[1]//2)*miniMapSize:
                    y=+mazeSize[1]-MBnum[1]//2
                else:
                    y=(y)//miniMapSize
                viewPoint=[x,y]
        else:
            if pressed_mouse[0]:#click left mouse button to set block
                x=(x)//MBsize-MBnum[0]//2+viewPoint[0]
                y=(y)//MBsize-MBnum[1]//2+viewPoint[1]
                if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
                    if [x,y] not in blockList: blockList.append([x,y])
            else:#click right mouse button to remove block
                x, y = pygame.mouse.get_pos()
                x=(x)//MBsize-MBnum[0]//2+viewPoint[0]
                y=(y)//MBsize-MBnum[1]//2+viewPoint[1]
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
        if viewPoint[1]>+MBnum[1]//2: viewPoint[1]-=1
    elif pressed_key[pygame.K_DOWN]:
        if viewPoint[1]<+mazeSize[1]-MBnum[1]//2: viewPoint[1]+=1
    elif pressed_key[pygame.K_RIGHT]:
        if viewPoint[0]<+mazeSize[0]-MBnum[0]//2: viewPoint[0]+=1
    elif pressed_key[pygame.K_LEFT]:
        if viewPoint[0]>+MBnum[0]//2: viewPoint[0]-=1
    #------------)
    updateMap()
