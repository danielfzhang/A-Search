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
#randomly load and analyze 1 maze image
filename=random.randint(1, 4)
filename='img/maze' + str(filename)+'.PNG'
mazeSize,Start,End,blockList=analyzeMaze(filename)
#parameters of map
MBsize=70
MBnum=[24,14]
miniMapSize=4
windowSize=(MBsize*MBnum[0], MBsize*MBnum[1])
viewPoint=[MBnum[0]//2,mazeSize[1]//2]
#pygame initialize
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, MBsize//2)
screen = pygame.display.set_mode(windowSize, 0, 32)
pygame.display.set_caption("Maze Defense")
#load images
Monster=pygame.image.load('img/monster.PNG')
Wall=pygame.image.load('img/wall.PNG')
Land=pygame.image.load('img/land.PNG')
Chest=pygame.image.load('img/chest.PNG')
Archer=pygame.image.load('img/archer.PNG')
Shovel=pygame.image.load('img/shovel.PNG')
Brick=pygame.image.load('img/brick.PNG')
#resize images
Monster = pygame.transform.scale(Monster, (MBsize, MBsize))
Wall= pygame.transform.scale(Wall, (MBsize, MBsize))
Land= pygame.transform.scale(Land, (MBsize, MBsize))
Chest= pygame.transform.scale(Chest, (MBsize, MBsize))
Archer= pygame.transform.scale(Archer, (MBsize, MBsize))
Shovel=pygame.transform.scale(Shovel, (MBsize, MBsize))
Brick=pygame.transform.scale(Brick, (MBsize, MBsize))
#game parameters
archerNum=2
shovelNum=2
brickNum=2
bagSize=[MBsize*2,MBsize*3]
bagPos=[MBsize*(MBnum[0]//2)-bagSize[0]//2, MBsize*(MBnum[1]//2)-bagSize[1]//2]
monsterPos=[-1,-1]
monsterSpeed=100
#randomly set chest
chestPos=random.choice(blockList)
while (chestPos[0]==0 or chestPos[1]==0 or
    chestPos[0]==mazeSize[0]-1 or chestPos[1]==mazeSize[1]-1):
    chestPos=random.choice(blockList)
#flags
bagOpen=False
archerUse=False
shovelUse=False
brickUse=False
monsterMove=False
leftClick=False
rightClick=False
#(functions-----------
def updateMap():
    for x in range(MBnum[0]//2*-1,MBnum[0]//2):#draw rows
        for y in range(MBnum[1]//2*-1,MBnum[1]//2):#draw cols
            if 0<=viewPoint[0]+x<mazeSize[0] and 0<=viewPoint[1]+y<mazeSize[1]:#view is within maze
                if [viewPoint[0]+x,viewPoint[1]+y] in blockList:#draw wall
                    screen.blit(Wall, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                else:
                    screen.blit(Land, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])#draw land
                    if [viewPoint[0]+x,viewPoint[1]+y]==chestPos:#chest
                        screen.blit(Chest, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                    if ([viewPoint[0]+x,viewPoint[1]+y]==monsterPos and monsterPos!=[-1,-1]):#draw monster
                        screen.blit(Monster, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
    #draw minimap
    pygame.draw.rect(screen,White,[0,0,mazeSize[0]*miniMapSize,mazeSize[1]*miniMapSize])
    for pixel in blockList:
        pygame.draw.rect(screen,Grey,[p*miniMapSize for p in pixel+[1,1]])
    pygame.draw.rect(screen,Green,[p*miniMapSize for p in End+[1,1]])
    pygame.draw.rect(screen,Green,[p*miniMapSize for p in Start+[1,1]])
    pygame.draw.rect(screen,Red,[p*miniMapSize for p in monsterPos+[1,1]])
    miniWindow=[viewPoint[0]-MBnum[0]//2,viewPoint[1]-MBnum[1]//2]
    pygame.draw.rect(screen,Red,[p*miniMapSize for p in miniWindow+MBnum],2)
    #draw bag
    if bagOpen:
        #bag and items
        pygame.draw.rect(screen,White,bagPos+bagSize)
        pygame.draw.rect(screen,Black,bagPos+bagSize,3)
        screen.blit(Archer, bagPos)
        screen.blit(Shovel, [bagPos[0],bagPos[1]+MBsize])
        screen.blit(Brick, [bagPos[0],bagPos[1]+MBsize*2])
        #num of items
        archerItem = font.render("X"+str(archerNum), True, Black)
        shovelItem = font.render("X"+str(shovelNum), True, Black)
        brickItem = font.render("X"+str(brickNum), True, Black)
        screen.blit(archerItem, [bagPos[0]+MBsize+MBsize//4,bagPos[1]+MBsize//4])
        screen.blit(shovelItem, [bagPos[0]+MBsize+MBsize//4,bagPos[1]+MBsize+MBsize//4])
        screen.blit(brickItem, [bagPos[0]+MBsize+MBsize//4,bagPos[1]+MBsize*2+MBsize//4])
    elif archerUse or shovelUse or brickUse:#items in use
        x, y = pygame.mouse.get_pos()
        x-= MBsize// 2
        y-= MBsize // 2
        if archerUse:
            screen.blit(Archer, (x, y))
        elif shovelUse:
            screen.blit(Shovel, (x, y))
        else:
            screen.blit(Brick, (x, y))
        pygame.mouse.set_visible(False)
    pygame.display.flip()
    clock.tick(60)
def geneMonster(destination):
    global monsterPos, monsterMove
    monsterPos=End[:]
    preStep=[[],[]]#track last two steps
    while monsterMove:
        archer=Astar(monsterPos,destination,blockList,mazeSize)
        nextStp=archer.nextStep()
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
#pygame main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:#press key
            if event.key == K_d:#bag
                if not bagOpen:
                    bagOpen=True
                    archerUse=shovelUse=brickUse=False
                    pygame.mouse.set_visible(True)
                else:
                    archerUse=shovelUse=brickUse=False
                    pygame.mouse.set_visible(True)
                    bagOpen=False
            elif event.key == K_RETURN and not monsterMove:#generage monster
                monsterMove=True
                t1=threading.Thread(target=geneMonster,args=(Start,))
                t1.setDaemon(True)
                t1.start()
        elif event.type == MOUSEBUTTONDOWN:
            pressed_mouse = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            if shovelUse or brickUse or archerUse:#use items
                if pressed_mouse[0]:
                    x=(x)//MBsize-MBnum[0]//2+viewPoint[0]
                    y=(y)//MBsize-MBnum[1]//2+viewPoint[1]
                    if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
                        if shovelUse:#remove block
                            if [x,y] in blockList:
                                blockList.remove([x,y])
                                shovelNum-=1
                        elif brickUse:#set block
                            if [x,y] not in blockList:
                                blockList.append([x,y])
                                brickNum-=1
                archerUse=shovelUse=brickUse=False
                pygame.mouse.set_visible(True)
            elif bagOpen:#select items
                if pressed_mouse[0]:
                    if bagPos[0]<=x<bagPos[0]+bagSize[0] and bagPos[1]<=y<bagPos[1]+MBsize:
                        if archerNum>0:
                            archerUse=True
                            bagOpen=False
                    elif bagPos[0]<=x<bagPos[0]+bagSize[0] and bagPos[1]+MBsize<=y<bagPos[1]+MBsize*2:
                        if shovelNum>0:
                            shovelUse=True
                            bagOpen=False
                    elif bagPos[0]<=x<bagPos[0]+bagSize[0] and bagPos[1]+MBsize*2<=y<bagPos[1]+MBsize*3:
                        if brickNum>0:
                            brickUse=True
                            bagOpen=False
                elif pressed_mouse[2]:
                    archerUse=shovelUse=brickUse=False
                    pygame.mouse.set_visible(True)
                    bagOpen=False

    #(press left mouse on minimap to move view-----
    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0]:
        x, y = pygame.mouse.get_pos()
        if 0<=x<miniMapSize*mazeSize[0] and 0<=y<miniMapSize*mazeSize[1]:
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
    #----------)
    #(use arrow keys to move view-------
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_UP] and viewPoint[1]>MBnum[1]//2:
        viewPoint[1]-=1
    elif pressed_key[pygame.K_DOWN] and viewPoint[1]<mazeSize[1]-MBnum[1]//2:
        viewPoint[1]+=1
    elif pressed_key[pygame.K_RIGHT] and viewPoint[0]<mazeSize[0]-MBnum[0]//2:
        viewPoint[0]+=1
    elif pressed_key[pygame.K_LEFT] and viewPoint[0]>MBnum[0]//2:
        viewPoint[0]-=1
    #------------)
    updateMap()
