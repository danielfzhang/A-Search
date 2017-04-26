#!/usr/bin/python3

#point is (x,y) coordinate
#node is the structure, which contains point and additional info

class Astar:
   def __init__(self, startPoint, endPoint, blockPoints, size, step_cost):
       #parameters initialization
       self.__size=size#window size
       self.__start=startPoint
       self.__end=endPoint
       self.__cost=step_cost
       self.__openlist = []
       self.__closelist = blockPoints
       self.__findpath=False
       self.shortestPath=[]
       #calculate f() + g() + h()
       #g() is the cost of the path from the start node to n
       #h() is a heuristic that estimates the cost of the cheapest path from n to the goal
       g=0
       h=abs(self.__start[0]-self.__end[0])+abs(self.__start[1]-self.__end[1])
       f=g+h
       parentPoint=[-1,-1]#the start point has no parent point
       #[0] (x,y), [1] is g(), [2] is h(),[3] is f(), [4] is parent
       cur_node=[startPoint]+[g]+[h]+[f]+[parentPoint]
       self.__openlist.append(cur_node)
       #min_point trace the point with minimal f()
       self.__minNode=cur_node

   def __AddOpen(self, pre_node, expanded_point):
       g=pre_node[1]+self.__cost
       h=abs(expanded_point[0]-self.__end[0])+abs(expanded_point[1]-self.__end[1])
       f=g+h
       cur_node=[expanded_point]+[g]+[h]+[f] +[pre_node[0]]
       #if the expanded point is in open list, do not add the point to open list
       #if the cost of expanded point is less than the point in open list, replace it.
       for i in range(len(self.__openlist)):
           if self.__openlist[i][0]==expanded_point:
               if f<self.__openlist[i][3]:
                   self.__openlist[i]=cur_node
               return
       #if the expanded point is not in open list, add it
       self.__openlist.append(cur_node)

   def __RemoveNode(self, node):
       #add the point to close list
       if node[4]==[-1,-1]:
           self.__closelist.append(node[0])
       else:
           for i in range(len(self.__closelist)):
               if node[4][0]==self.__closelist[i][0] and node[4][1]==self.__closelist[i][1]:
                   self.__closelist.append([node[0][0],node[0][1],i])
                   break
       #remove the point from open list
       self.__openlist.remove(node)
       #if there is element in the list
       if self.__openlist!=[]:
           #update min_point
           self.__minNode=[[0,0]]+[0]+[3*self.__size]+[3*self.__size]
           for each_point in self.__openlist:
               if each_point[2]<=self.__minNode[2] and each_point[3]<=self.__minNode[3]:
                   self.__minNode=each_point

   def __shortestPath(self):
       cur_index=-1
       self.shortestPath.insert(0,self.__end)
       while len(self.__closelist[cur_index])!=2:
           point=[self.__closelist[cur_index][0],self.__closelist[cur_index][1]]
           self.shortestPath.insert(0,point)
           cur_index=self.__closelist[cur_index][2]
       self.shortestPath.insert(0,self.__start)

   #only do search once, and return the point searched
   def oneSearch(self):
       if self.__findpath:
           return "find path"
       elif self.__openlist==[]:
           return "no path"
       else:
           expanded_point=self.__minNode[0]
           if expanded_point==self.__end:
               self.__findpath=True
               self.__shortestPath()
           else:
               direct4=[[0,-1],[0,1],[-1,0],[1,0]]#up,down,left,right
               #add available points to open list,up,down,left,right
               for direction in direct4:
                   point_x=self.__minNode[0][0]+direction[0]
                   point_y=self.__minNode[0][1]+direction[1]
                   #the point is within the window
                   if point_x>=0 and point_x<self.__size and point_y>=0 and point_y<self.__size:
                       point=[point_x,point_y]
                       duplicated=False
                       for i in range(len(self.__closelist)):
                           if point[0]==self.__closelist[i][0] and point[1]==self.__closelist[i][1]:
                               duplicated=True
                       #if the point is not in close list
                       if not duplicated:
                           self.__AddOpen(self.__minNode, point)
           #remove the node
           self.__RemoveNode(self.__minNode)
           return expanded_point
