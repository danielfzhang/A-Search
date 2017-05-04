#!/usr/bin/python3
from helper import *
from pygame.locals import *
from sys import exit
import pygame, os, threading, random, math, time
#set window to most left top on the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
#colors
Grey=[105,105,105]
White=[255,255,255]
Black=[0,0,0]
Red=[255,0,0]
Green=[0,255,0]
Turquoise=[0,245,255]
#randomly load and analyze a maze image
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
Zombie=pygame.image.load('img/zombie.PNG')
Wall=pygame.image.load('img/wall.PNG')
Road=pygame.image.load('img/road.PNG')
Chest=pygame.image.load('img/chest.PNG')
Chili=pygame.image.load('img/chili.PNG')
Chili0=pygame.image.load('img/chili0.PNG')
Shovel=pygame.image.load('img/shovel.PNG')
Brick=pygame.image.load('img/brick.PNG')
Attack=pygame.image.load('img/attack.PNG')
Damaged=pygame.image.load('img/damaged.PNG')
Bomb=pygame.image.load('img/bomb.PNG')
#resize images
Zombie = pygame.transform.scale(Zombie, (MBsize, MBsize))
Wall= pygame.transform.scale(Wall, (MBsize, MBsize))
Road= pygame.transform.scale(Road, (MBsize, MBsize))
Chest= pygame.transform.scale(Chest, (MBsize, MBsize))
Chili= pygame.transform.scale(Chili, (MBsize, MBsize))
Chili0= pygame.transform.scale(Chili0, (MBsize, MBsize))
Shovel=pygame.transform.scale(Shovel, (MBsize, MBsize))
Brick=pygame.transform.scale(Brick, (MBsize, MBsize))
Attack=pygame.transform.scale(Attack, (MBsize, MBsize))
Damaged=pygame.transform.scale(Damaged, (MBsize, MBsize))
Bomb=pygame.transform.scale(Bomb, (MBsize*3, MBsize*3))
#parameters of the game
chiliList=[]
attackList=[]
blockNum=0
chiliNum=2
shovelNum=50
brickNum=0
zombieLife=0
zombiePath=[]
bagSize=[MBsize*2,MBsize*3]
bagPos=[MBsize*(MBnum[0]//2)-bagSize[0]//2, MBsize*(MBnum[1]//2)-bagSize[1]//2]
zombiePos=[-1,-1]
#randomly set chest....find chest to win the game
chestPos=random.choice(blockList)
while (chestPos[0]==0 or chestPos[1]==0 or
    chestPos[0]==mazeSize[0]-1 or chestPos[1]==mazeSize[1]-1):
    chestPos=random.choice(blockList)
print(chestPos)#cheating!!!!!!!!
#flags
bagOpen=False
chiliUse=False
shovelUse=False
brickUse=False
explode=False
zombieExit=False
#(functions-----------
def updateMap():
    global blockList, zombieLife
    bomX,bomY=[[],[]]
    for x in range(MBnum[0]//2*-1,MBnum[0]//2):# rows
        for y in range(MBnum[1]//2*-1,MBnum[1]//2):# cols
            if 0<=viewPoint[0]+x<mazeSize[0] and 0<=viewPoint[1]+y<mazeSize[1]:#view is within maze
                if [viewPoint[0]+x,viewPoint[1]+y] in blockList:#wall
                    screen.blit(Wall, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                elif [viewPoint[0]+x,viewPoint[1]+y] in [p[0:2] for p in chiliList]:# Chili
                    if [viewPoint[0]+x,viewPoint[1]+y] in [p[0:2] for p in attackList]:
                        screen.blit(Attack, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])#chili attack
                    else: screen.blit(Chili, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])#normal chili
                elif [viewPoint[0]+x,viewPoint[1]+y]==zombiePos and zombieLife>0:#Zombie
                    if attackList==[]:
                        screen.blit(Zombie, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])#normal zombie
                    else: screen.blit(Damaged, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])#damaged zombie
                elif [viewPoint[0]+x,viewPoint[1]+y]==zombiePos and explode:#zombie dies and explode
                    bomX=(x+MBnum[0]//2-1)*MBsize
                    bomY=(y+MBnum[1]//2-1)*MBsize
                elif [viewPoint[0]+x,viewPoint[1]+y]==chestPos:#find chest game over
                    screen.blit(Chest, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])
                    pygame.display.update()
                    pygame.time.delay(5000)
                    blockList=[]
                    zombieLife=0
                    exit()
                else:
                    screen.blit(Road, [(x+MBnum[0]//2)*MBsize,(y+MBnum[1]//2)*MBsize])# road
    if explode and [bomX,bomY]!=[[],[]]:
        screen.blit(Bomb, [bomX,bomY])
    #draw bag
    if bagOpen:
        #bag and items
        pygame.draw.rect(screen,White,bagPos+bagSize)
        pygame.draw.rect(screen,Black,bagPos+bagSize,3)
        screen.blit(Chili0, bagPos)
        screen.blit(Shovel, [bagPos[0],bagPos[1]+MBsize])
        screen.blit(Brick, [bagPos[0],bagPos[1]+MBsize*2])
        #num of items
        chiliItem = font.render("X"+str(chiliNum), True, Black)
        shovelItem = font.render("X"+str(shovelNum), True, Black)
        brickItem = font.render("X"+str(brickNum), True, Black)
        screen.blit(chiliItem, [bagPos[0]+MBsize+MBsize//4,bagPos[1]+MBsize//4])
        screen.blit(shovelItem, [bagPos[0]+MBsize+MBsize//4,bagPos[1]+MBsize+MBsize//4])
        screen.blit(brickItem, [bagPos[0]+MBsize+MBsize//4,bagPos[1]+MBsize*2+MBsize//4])
    elif chiliUse or shovelUse or brickUse:#items in use
        x, y = pygame.mouse.get_pos()
        x-= MBsize// 2
        y-= MBsize // 2
        if chiliUse:
            screen.blit(Chili0, (x, y))
        elif shovelUse:
            screen.blit(Shovel, (x, y))
        else: screen.blit(Brick, (x, y))
        pygame.mouse.set_visible(False)
    #draw minimap
    pygame.draw.rect(screen,White,[0,0,mazeSize[0]*miniMapSize,mazeSize[1]*miniMapSize])
    for pixel in blockList:
        pygame.draw.rect(screen,Grey,[p*miniMapSize for p in pixel+[1,1]])#wall
    for pixel in [p[0:2] for p in chiliList]:
        pygame.draw.rect(screen,Green,[p*miniMapSize for p in pixel[0:2]+[1,1]])#draw Chili
    pygame.draw.rect(screen,Turquoise,[p*miniMapSize for p in End+[1,1]])#end
    pygame.draw.rect(screen,Turquoise,[p*miniMapSize for p in Start+[1,1]])#start
    if zombieLife>0:#zombie
        pygame.draw.rect(screen,Red,[p*miniMapSize for p in zombiePos+[1,1]])
    miniWindow=[viewPoint[0]-MBnum[0]//2,viewPoint[1]-MBnum[1]//2]
    pygame.draw.rect(screen,Red,[p*miniMapSize for p in miniWindow+MBnum],2)
    #update screen
    pygame.display.update()
    clock.tick(60)

def makeZombie(destination):
    global blockNum, zombiePath, zombieLife, zombiePos, explode, chiliList
    zombiePos=End[:]
    if blockNum!=len(blockList):#calculate shortestPath again if walls# change
        blockNum=len(blockList)
        Asearch=Astar(zombiePos,destination,blockList,mazeSize)
        Asearch.nextStep()
        zombiePath=Asearch.shortestPath
    moveSpeed=700
    eatSpeed=2000
    zombieLife=3
    for nextStp in zombiePath:
        if zombieLife<1:
            break#zombie is killed
        elif nextStp in [p[0:2] for p in chiliList]:
            pygame.time.delay(eatSpeed)
            if zombieLife<1:
                break#zombie is killed
            else:
                for p in chiliList:
                    if nextStp==p[0:2]:
                        p[4]='die'
        zombiePos=nextStp#move
        pygame.time.delay(moveSpeed)
    if explode:#explode
        pygame.time.delay(300)#explode animation time
        explode=False
        for x in range(-1,2):
            for y in range(-1,2):
                if 0<x+zombiePos[0]<mazeSize[0]-1 and 0<x+zombiePos[1]<mazeSize[1]-1:#wall cannot be removed
                    if [x+zombiePos[0],y+zombiePos[1]] in blockList:#remove walls
                        blockList.remove([x+zombiePos[0],y+zombiePos[1]])
                    elif [x+zombiePos[0],y+zombiePos[1]] in [p[0:2] for p in chiliList]:#remove chilies
                        for p in chiliList:
                            if [x+zombiePos[0],y+zombiePos[1]]==p[0:2]:
                                p[4]='die'
    if not zombieExit:
        makeZombie(destination)#new zombie

def makeChili():
    global zombieLife,shovelNum,chiliNum, explode
    attackSpeed=2#second
    damage=1
    while chiliList!=[]:#chili is alive
        for cc in chiliList:
            if cc[4]=='die':
                if cc in attackList:
                    attackList.remove(cc)
                chiliList.remove(cc)
                continue
            if cc[3]=='none'and zombieLife>0:
                for i in range(-2,3):#zombie is alve and within attack range
                    if [cc[0]+i,cc[1]]==zombiePos or [cc[0],cc[1]+i]==zombiePos:
                        attackList.append(cc)
                        cc[2]=time.time()#set up timer
                        cc[3]='attacking'
            elif cc[3]=='attacking':
                if time.time()-cc[2]>=0.3:
                    zombieLife-=damage
                    if zombieLife==0:
                        if random.randint(1, 3)==1:#reward
                            shovelNum+=2
                        else: chiliNum+=2
                        if random.randint(1, 3)==1:#33% chance explode
                            explode=True
                    attackList.remove(cc)
                    cc[3]='cooldown'
            elif cc[3]=='cooldown':
                if time.time()-cc[2]>=attackSpeed:
                    cc[3]='none'

#-------------functions)
updateMap()
#start zombie thread
monsterThread=threading.Thread( target=makeZombie, args=(Start,) )
monsterThread.setDaemon(True)
monsterThread.start()
#pygame main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:#quite all threading and exit
            zombieExit=True
            chiliList==[]
            exit()
        #press key
        elif event.type == KEYDOWN:
            if event.key == K_q:#bag
                if not bagOpen:
                    bagOpen=True
                    chiliUse=shovelUse=brickUse=False
                    pygame.mouse.set_visible(True)
                else:
                    chiliUse=shovelUse=brickUse=False
                    pygame.mouse.set_visible(True)
                    bagOpen=False
        #press mouse
        elif event.type == MOUSEBUTTONDOWN:
            pressed_mouse = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            if shovelUse or brickUse or chiliUse:#use items
                if pressed_mouse[0]:
                    x=(x)//MBsize-MBnum[0]//2+viewPoint[0]
                    y=(y)//MBsize-MBnum[1]//2+viewPoint[1]
                    if 0<x<mazeSize[0]-1 and 0<y<mazeSize[1]-1:
                        if shovelUse:#remove block
                            if [x,y] in blockList:
                                shovelNum-=1
                                blockList.remove([x,y])
                            elif [x,y] in [p[0:2] for p in chiliList]:
                                shovelNum-=1
                                for p in chiliList:
                                    if [x,y]==p[0:2]:
                                        p[4]='die'
                        elif brickUse:#set block
                            if [x,y] not in blockList:
                                blockList.append([x,y])
                                brickNum-=1
                        else:#use chili
                            chiliNum-=1
                            if chiliList==[]:
                                chiliList.append([x,y,0,'none','alive'])
                                chiliThread=threading.Thread(target=makeChili)
                                chiliThread.setDaemon(True)
                                chiliThread.start()
                            else: chiliList.append([x,y,0,'none','alive'])
                chiliUse=shovelUse=brickUse=False
                pygame.mouse.set_visible(True)
            elif bagOpen:#select items
                if pressed_mouse[0]:
                    if bagPos[0]<=x<bagPos[0]+bagSize[0] and bagPos[1]<=y<bagPos[1]+MBsize:
                        if chiliNum>0:
                            chiliUse=True
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
                    chiliUse=shovelUse=brickUse=False
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
    #(key functions-------
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_w] and viewPoint[1]>MBnum[1]//2:
        viewPoint[1]-=1
    elif pressed_key[pygame.K_s] and viewPoint[1]<mazeSize[1]-MBnum[1]//2:
        viewPoint[1]+=1
    elif pressed_key[pygame.K_d] and viewPoint[0]<mazeSize[0]-MBnum[0]//2:
        viewPoint[0]+=1
    elif pressed_key[pygame.K_a] and viewPoint[0]>MBnum[0]//2:
        viewPoint[0]-=1
    elif pressed_key[pygame.K_e] and zombieLife>0:#view to zombie
        x,y=zombiePos
        if x<MBnum[0]//2:
            x=MBnum[0]//2
        elif x>=(mazeSize[0]-MBnum[0]//2):
            x=mazeSize[0]-MBnum[0]//2
        if y<MBnum[1]//2:
            y=MBnum[1]//2
        elif y>=mazeSize[1]-MBnum[1]//2:
            y=mazeSize[1]-MBnum[1]//2
        viewPoint=[x,y]
    #------------)
    updateMap()
