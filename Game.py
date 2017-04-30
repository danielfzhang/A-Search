#!/usr/bin/python3
from helper import *
from pygame.locals import *
from sys import exit
import pygame, math, os
#Maze class
class MazeC:
    def __init__(self,init_pos=[0,0]):
        #parameter definition
        self.White=[255,255,255]
        self.Black=[0,0,0]
        self.CadetBlue=[152,245,255]
        self.pos=init_pos
        self.update()
    def update(self):
        screen.fill(self.White)
        for pixel in BlockList:
            pygame.draw.rect(screen,self.Black,[p[0]*MBsize+p[1] for p in zip(pixel,self.pos)]+[MBsize,MBsize])
        pygame.draw.rect(screen,self.CadetBlue,[p[0]*MBsize+p[1] for p in zip(End,self.pos)]+[MBsize,MBsize])
        pygame.draw.rect(screen,self.CadetBlue,[p[0]*MBsize+p[1] for p in zip(Start,self.pos)]+[MBsize,MBsize])
#monster class
class MonsterC:
    def __init__(self,Maze,init_pos=[0,0]):
        self.Monster=pygame.image.load('pic/monster.PNG').convert_alpha()
        self.Monster = pygame.transform.scale(self.Monster, (MBsize, MBsize))
        self.pos=init_pos
        self.maze=Maze
        self.update()
    def update(self):
        self.maze.update()
        screen.blit(self.Monster, [p[0]*MBsize+p[1] for p in zip(Monster_pos,self.pos)])
#damage animation
def damage(monster):
    for i in range(3):
        screen.fill([255,255,255])
        pygame.display.update()
        pygame.time.delay(100)
        monster.update()
        pygame.display.update()
        pygame.time.delay(100)

#set the position of window as (0,30) on the displayer
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
#pygame initialization
pygame.init()
winSize=(1200, 800)
MBsize=54
screen = pygame.display.set_mode(winSize, 0, 32)
pygame.display.set_caption("Maze Defense")
#analyze image of the maze
MazeSize,Start,End,BlockList=analyzeMaze('pic/maze1.PNG')
Monster_pos=End[:]
MazePos=[(winSize[0]-MazeSize[0]*MBsize)//2]
MazePos+=[(winSize[1]-MazeSize[1]*MBsize)//2]
#draw maze
Maze=MazeC(MazePos)
Monster=MonsterC(Maze,MazePos)
pygame.display.update()
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
                Asearch=Astar(Monster_pos,Start,BlockList,MazeSize)
                result=Asearch.oneSearch()
                while result!="find path" and result!="no path":
                    result=Asearch.oneSearch()
                if result=="find path":
                    for p in Asearch.shortestPath:
                        Monster_pos=p
                        Monster.update()
                        pygame.display.update()
                        pygame.time.delay(200)
                    damage(Monster)
            elif event.key == K_UP:
                if [Monster_pos[0],Monster_pos[1]-1] not in BlockList:
                    Monster_pos[1]-=1
                    Monster.update()
            elif event.key == K_DOWN:
                if [Monster_pos[0],Monster_pos[1]+1] not in BlockList:
                    Monster_pos[1]+=1
                    Monster.update()
            elif event.key == K_RIGHT:
                if [Monster_pos[0]+1,Monster_pos[1]] not in BlockList:
                    if Monster_pos[0]+1<MazeSize[0]:
                        Monster_pos[0]+=1
                        Monster.update()
            elif event.key == K_LEFT:
                if [Monster_pos[0]-1,Monster_pos[1]] not in BlockList:
                    if Monster_pos[0]>0:
                        Monster_pos[0]-=1
                        Monster.update()
    if buttonDown:
        x, y = pygame.mouse.get_pos()
        x=math.floor((x-MazePos[0])/MBsize)
        y=math.floor((y-MazePos[1])/MBsize)
        if [x,y] not in BlockList:
            BlockList.append([x,y])
        Monster.update()
    pygame.display.update()
