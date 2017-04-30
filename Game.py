#!/usr/bin/python3
from helper import *
from pygame.locals import *
from sys import exit
import pygame, math, os, threading
#classes and functions
#--------------------
#Maze class, display all elements in the Maze
class MazeC:
    def __init__(self):
        global MazePos,MBsize
        #colors
        self.White=[255,255,255]
        self.Black=[0,0,0]
        self.CadetBlue=[152,245,255]
        #load image of monster
        self.Monster=pygame.image.load('img/monster.PNG').convert_alpha()
        self.Monster = pygame.transform.scale(self.Monster, (MBsize, MBsize))
        self.pos=MazePos
        #display Maze
        self.update()
    def update(self):
        global Start,End,BlockList,Monster_pos,MBsize
        screen.fill(self.White)
        #draw blocks
        for pixel in BlockList:
            pygame.draw.rect(screen,self.Black,[p[0]*MBsize+p[1] for p in zip(pixel,self.pos)]+[MBsize,MBsize])
        #draw end
        pygame.draw.rect(screen,self.CadetBlue,[p[0]*MBsize+p[1] for p in zip(End,self.pos)]+[MBsize,MBsize])
        #draw Start
        pygame.draw.rect(screen,self.CadetBlue,[p[0]*MBsize+p[1] for p in zip(Start,self.pos)]+[MBsize,MBsize])
        #draw monster if it is in the Maze
        if Monster_pos>=[0,0]:
            screen.blit(self.Monster, [p[0]*MBsize+p[1] for p in zip(Monster_pos,self.pos)])
        pygame.display.update()

#monster walk to destination in shortestPath
def findPath():
    global Monster_pos,Start,BlockList,MazeSize,End,MonsterMove,exitFindpath
    movespeed=10
    dieTime=1000
    while Monster_pos!=Start:
        if exitFindpath:
            exitFindpath=False
            MonsterMove=False
            return
        Asearch=Astar(Monster_pos,Start,BlockList,MazeSize)
        result=Asearch.oneSearch()
        while result!="find path" and result!="no path":
            result=Asearch.oneSearch()
        if result=="find path":
            if len(Asearch.shortestPath)>1:
                Monster_pos=Asearch.shortestPath[1]
                pygame.time.delay(movespeed)
    Monster_pos=[-1,-1]
    pygame.time.delay(dieTime)
    Monster_pos=End[:]
    MonsterMove=False

if __name__ == "__main__":
    global MazeSize,Start,End,BlockList,Monster_pos,MazePos,MBsize,Maze
    #set the position of window as (0,30) on the displayer
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
    #pygame initialization
    pygame.init()
    winSize=(1200, 800)
    MBsize=54
    screen = pygame.display.set_mode(winSize, 0, 32)
    pygame.display.set_caption("Maze Defense")
    #analyze image of the maze
    MazeSize,Start,End,BlockList=analyzeMaze('img/maze1.PNG')
    Monster_pos=End[:]
    MazePos=[(winSize[0]-MazeSize[0]*MBsize)//2]
    MazePos+=[(winSize[1]-MazeSize[1]*MBsize)//2]
    #draw maze
    Maze=MazeC()
    #pygame loop
    drawBLK=False
    drawWHT=False
    MonsterMove=False
    exitFindpath=False #interrupt findPath() thread
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type ==  MOUSEBUTTONDOWN:
                pressed_mouse = pygame.mouse.get_pressed()
                if pressed_mouse[0]:#left click to set blocks
                    drawBLK=True
                elif pressed_mouse[2]:#right click to remove blocks
                    drawWHT=True
            elif event.type ==  MOUSEBUTTONUP:
                drawBLK=False
                drawWHT=False
            elif event.type == KEYDOWN and Monster_pos!=[-1,-1]:
                if MonsterMove:#interrupt findPath() thread
                    exitFindpath=True
                if event.key == K_RETURN and not MonsterMove:#create thread to find path to destination
                    MonsterMove=True
                    t1=threading.Thread(target=findPath)
                    t1.setDaemon(True)
                    t1.start()
                #control monster by up, down, right, left arrow keys 
                elif event.key == K_UP:
                    if [Monster_pos[0],Monster_pos[1]-1] not in BlockList:
                        Monster_pos[1]-=1
                elif event.key == K_DOWN:
                    if [Monster_pos[0],Monster_pos[1]+1] not in BlockList:
                        Monster_pos[1]+=1
                elif event.key == K_RIGHT:
                    if [Monster_pos[0]+1,Monster_pos[1]] not in BlockList:
                        if Monster_pos[0]+1<MazeSize[0]:
                            Monster_pos[0]+=1
                elif event.key == K_LEFT:
                    if [Monster_pos[0]-1,Monster_pos[1]] not in BlockList:
                        if Monster_pos[0]>0:
                            Monster_pos[0]-=1
        #left click set blocks
        if drawBLK:
            x, y = pygame.mouse.get_pos()
            x=math.floor((x-MazePos[0])/MBsize)
            y=math.floor((y-MazePos[1])/MBsize)
            if 0<x<MazeSize[0]-1 and 0<y<MazeSize[1]-1:
                if [x,y] not in BlockList:
                    BlockList.append([x,y])
        #right click remove blocks
        elif drawWHT:
            x, y = pygame.mouse.get_pos()
            x=math.floor((x-MazePos[0])/MBsize)
            y=math.floor((y-MazePos[1])/MBsize)
            if 0<x<MazeSize[0]-1 and 0<y<MazeSize[1]-1:
                if [x,y] in BlockList:
                    BlockList.remove([x,y])
        Maze.update()
