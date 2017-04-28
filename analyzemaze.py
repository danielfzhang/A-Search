#!/usr/bin/python3
import cv2
import numpy as np
import math
def analyzeMaze(file):
    """Analyze an image of a Maze.

       return MazeSize, Start point, End point,
       and BlockList"""
    #color definition
    WHITE=np.array([255,255,255])
    BLACK=np.array([0,0,0])
    #read the image file
    img = cv2.imread(file)
    #find origin_Maze,,blk_size
    blk_size=0
    findMaze=False
    findblk_size=False
    for y, row in enumerate(img):
        for x,pixel in enumerate(row):
            if findMaze:
                if (pixel==WHITE).all():
                    blk_size+=1
                elif (pixel!=BLACK).all():
                    break
            if (pixel==BLACK).all() and not findMaze:
                origin_Maze=[y,x]
                findMaze=True
        if findMaze:
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
    for i in range(MazeSize[0]):
        if [i,0] not in BlockList:
            Start=[i,0]
            break
    for i in range(MazeSize[0]):
        if [i,MazeSize[1]-1] not in BlockList:
            End=[i,MazeSize[1]-1]
            break
    return MazeSize,Start,End,BlockList
