#!/usr/bin/python3
import cv2
import numpy as np
import math
def analyzeMaze(file):
    """Analyze an image of a Maze.

    return MazeSize, Start point, Endpoint, BlockList"""
    #color definition
    WHITE=np.array([255,255,255])
    BLACK=np.array([0,0,0])
    #read the image file
    img = cv2.imread(file)
    #find origin_Maze,,blk_size
    blk_size=0
    findMaze=False
    findblk_size=False
    for y,row in enumerate(img):
        for x,pixel in enumerate(row):
            if (pixel==BLACK).all():
                origin_Maze=[y,x]
                findMaze=True
                break
        if findMaze:
            break
    for i in range(origin_Maze[0],img.shape[0]):
        if (img[i][origin_Maze[1]]==WHITE).all():
            blk_size+=1
        elif (pixel!=BLACK).all():
            break
    #compute block list
    BlockList=[]
    for j in range(0,2):
        for y, row in enumerate(img[origin_Maze[0]+j:-1:blk_size+1]):
            for i in range(0,2):
                for x, pixel in enumerate(row[origin_Maze[1]+i:-1:blk_size+1]):
                    if (pixel==BLACK).all():
                        BlockList.append([y*2+j,x*2+i])
    #the structure of image is [y][x], but it is [x][y] in pygame
    #we need to switch the x and y for Start,End,BlockList
    BlockList.sort()
    y=max(BlockList)[0]
    for e in BlockList:
        exch=e[0]
        e[0]=e[1]
        e[1]=exch
    x=max(BlockList)[0]
    MazeSize=[x+1,y+1]
    #find Start and End point
    for i in range(MazeSize[1]):
        if [0,i] not in BlockList:
            Start=[0,i]
            break
    for i in range(MazeSize[0]):
        if [MazeSize[0]-1,i] not in BlockList:
            End=[MazeSize[0]-1,i]
            break
    return MazeSize,Start,End,BlockList

#point is (x,y) coordinate
#node is the structure, which contains point and additional info
class Astar:
    """
    Perform A* algorithm to find the shortest path.

    find the shortest path from __start point to __end point
    blockPoints are the points that cannot be positioned
    size is the window size"""
    def __init__(self, startPoint, endPoint, blockPoints, size, step_cost=1):
        #parameters initialization
        self.__start=startPoint
        self.__end=endPoint
        self.__closelist = blockPoints[:]
        self.__size=size#window size
        self.__cost=step_cost
        self.__openlist = []
        self.__findpath=False
        self.shortestPath=[]
        #calculate f() + g() + h()
        #g() is the cost of the path from the __start node to n
        #h() is a heuristic that estimates the cost of the cheapest path from n to the goal
        g=0
        h=abs(self.__start[0]-self.__end[0])+abs(self.__start[1]-self.__end[1])
        f=g+h
        parentPoint=[-1,-1]#the __start point has no parent point
        #[0] (x,y), [1] is g(), [2] is h(),[3] is f(), [4] is parent
        cur_node=[startPoint]+[g]+[h]+[f]+[parentPoint]
        #min_point trace the point with minimal f()
        self.__minNode=cur_node
        self.__openlist.append(cur_node)

    def __AddOpen(self, expanded_point):
        g=self.__minNode[1]+self.__cost
        h=abs(expanded_point[0]-self.__end[0])+abs(expanded_point[1]-self.__end[1])
        f=g+h
        cur_node=[expanded_point]+[g]+[h]+[f]+[self.__minNode[0]]
        #if the expanded point is in open list, do not add the point to open list
        #if the cost of expanded point is less than the point in open list, replace it.
        for node in self.__openlist:
            if cur_node[0]==node[0]:
                if cur_node[3]<node[3]:
                    node=cur_node
                return
        #if the expanded point is not in open list, add it
        self.__openlist.append(cur_node)

    def __RemoveMin(self):
        #add the point to close list
        self.__closelist.append(self.__minNode)
        #remove the point from open list
        self.__openlist.remove(self.__minNode)
        #if there is element in the list
        if self.__openlist!=[]:
            #update min_point
            self.__minNode=[[0,0]]+[0]+[3*max(self.__size)]+[3*max(self.__size)]+[[-1,-1]]
            for node in self.__openlist:
                if node[2:4]<=self.__minNode[2:4]:
                    self.__minNode=node

    def __shortestPath(self):
        cur_index=-1
        self.shortestPath.insert(0,self.__closelist[cur_index][0])
        parent=self.__closelist[cur_index][4]
        while parent!=[-1,-1]:
            if self.__closelist[cur_index][0]==parent:
                self.shortestPath.insert(0,parent)
                parent=self.__closelist[cur_index][4]
            cur_index-=1

    #only do search once, and return the point searched
    def oneSearch(self):
        if self.__findpath:
            return "find path"
        elif self.__openlist==[]:
            return "no path"
        else:
            expanded_point=self.__minNode[0][:]
            if expanded_point==self.__end:
                self.__findpath=True
            else:
                direct4=[[0,-1],[0,1],[-1,0],[1,0]]#up,down,left,right
                #add available points to open list,up,down,left,right
                for direction in direct4:
                    point_x=self.__minNode[0][0]+direction[0]
                    point_y=self.__minNode[0][1]+direction[1]
                    #the point is within the window
                    if 0<=point_x<self.__size[0] and 0<=point_y<self.__size[1]:
                        point=[point_x,point_y]
                        duplicated=False
                        for node in self.__closelist:
                            if point==node[0] or point==node:
                                duplicated=True
                                break
                        #if the point is not in close list
                        if not duplicated:
                           self.__AddOpen(point)
            #remove the node
            self.__RemoveMin()
            #find the shortest path, store it in the list
            if self.__findpath:
                self.__shortestPath()
            return expanded_point
