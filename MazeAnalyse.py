import cv2, numpy
def analyzeMaze(file):
    """Analyze an image of a Maze.

    return MazeSize, Start point, Endpoint, BlockList"""
    #colors
    White=numpy.array([255,255,255])
    Black=numpy.array([0,0,0])
    #read the image file
    img = cv2.imread(file)
    #find origin_Maze,,blk_size
    blk_size=0
    findMaze=False
    findblk_size=False
    for y,row in enumerate(img):
        for x,pixel in enumerate(row):
            if (pixel==Black).all():
                origin_Maze=[y,x]
                findMaze=True
                break
        if findMaze: break
    if not findMaze:#cannot find maze
        errmesg='color of wall in maze must be black and background color must not be black'
        return errmesg,0,0,0

    findblk_size=False
    for i in range(origin_Maze[0],img.shape[0]):#check entrance on the left
        if (img[i][origin_Maze[1]]==Black).all() and blk_size!=0:
            findblk_size=True
            break
        elif (img[i][origin_Maze[1]]!=Black).all():
            blk_size+=1
    if not findblk_size:
        blk_size=0
        for i in range(origin_Maze[1],img.shape[1]):#check entrance on the top
            if (img[origin_Maze[0]][i]==Black).all() and blk_size!=0:
                findblk_size=True
                break
            elif (img[origin_Maze[0]][i]!=Black).all():
                blk_size+=1
    if not findblk_size:#cannot find entrance
        errmesg='no entrance on the left or top of maze is found'
        return errmesg,0,0,0
    #compute block list
    BlockList=[]
    for j in range(0,2):
        for y, row in enumerate(img[origin_Maze[0]+j:-1:blk_size+1]):
            for i in range(0,2):
                for x, pixel in enumerate(row[origin_Maze[1]+i:-1:blk_size+1]):
                    if (pixel==Black).all():
                        BlockList.append([y*2+j,x*2+i])
    #the structure of image is [y][x], but it is [x][y] in pygame
    #we need to switch the x and y for Start,End,BlockList
    BlockList.sort()
    y=max(BlockList)[0]
    for i,e in enumerate(BlockList):
        BlockList[i]=[e[1],e[0]]
    x=max(BlockList)[0]
    MazeSize=[x+1,y+1]
    #find Start and End point
    Start=[-1,-1]
    End=[-1,-1]
    for i in range(MazeSize[1]):#on left and right
        if [0,i] not in BlockList:
            Start=[0,i]
        if [MazeSize[0]-1,i] not in BlockList:
            End=[MazeSize[0]-1,i]
    if Start==[-1,-1] or End==[-1,-1]:
        for i in range(MazeSize[0]):#on top and bottom
            if Start==[-1,-1] and [i,0] not in BlockList:
                Start=[i,0]
            if End==[-1,-1] and [i,MazeSize[1]-1] not in BlockList:
                End=[i,MazeSize[1]-1]
    if Start==[-1,-1] or End==[-1,-1]:
        errmesg='no entrance or exit of maze is found'
        return errmesg,0,0,0
    else: return MazeSize,Start,End,BlockList
