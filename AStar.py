#point is (x,y) coordinate
#node is the structure, which contains point and additional info
import sys
class Astar:
    """
    Perform A* algorithm to find the shortest path.

    find the shortest path from __start point to __end point
    blockSet are the points that cannot be positioned
    size is the window size"""
    def __init__(self, startPoint, endPoint, blockList, size):
        #parameters initialization
        self.__start=startPoint[:]
        self.__end=endPoint[:]
        self.__closelist = blockList[:]
        self.__size=size[:]#window size
        self.__openlist = []
        self.shortestPath=[]
        self.__cost=1
        self.__findpath=False
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
            if cur_node[0]==node[0] and cur_node[3]<node[3]:
                node=cur_node
                return
        #if the expanded point is not in open list, add it
        else: self.__openlist.append(cur_node)

    def __RemoveMin(self):
        #add the point to close list
        self.__closelist.append(self.__minNode)
        #remove the point from open list
        self.__openlist.remove(self.__minNode)
        #if there is element in the list
        if self.__openlist!=[]:
            #update min_point
            self.__minNode=[[0,0]]+[0]+[sys.maxsize]+[sys.maxsize]+[[-1,-1]]
            for node in self.__openlist:
                if node[3]<self.__minNode[3]:
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
    def nextStep(self):
        while True:
            if self.__minNode[0]==self.__end:
                self.__RemoveMin()#remove the node
                self.__shortestPath()
                if len(self.shortestPath)==1:
                    return self.__end
                else: return self.shortestPath[1]
            elif self.__openlist!=[]:
                direct4=[[0,-1],[0,1],[-1,0],[1,0]]#up,down,left,right
                #add available points to open list,up,down,left,right
                for direction in direct4:
                    point_x=self.__minNode[0][0]+direction[0]
                    point_y=self.__minNode[0][1]+direction[1]
                    #the point is within the window
                    if 0<=point_x<self.__size[0] and 0<=point_y<self.__size[1]:
                        point=[point_x,point_y]
                        for node in self.__closelist:
                            if point==node[0] or point==node: break
                        else: self.__AddOpen(point)#the point is not in close list
                self.__RemoveMin()#remove the node
            else: return
