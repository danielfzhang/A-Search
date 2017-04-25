#!/usr/bin/python3
class Astar:
   def __init__(self, start, end, blocks, size, step_cost):
       #parameters initialization
       self.size=size#window size
       self.start=start
       self.end=end
       self.cost=step_cost
       self.openlist = []
       self.closelist = blocks
       self.findpath=False
       #calculate f() + g() + h()
       g=0
       h=abs(self.start[0]-self.end[0])+abs(self.start[1]-self.end[1])
       f=g+h
       cur_point=[start]+[g]+[h]+[f]
       #[0] is index, [1] is g(), [2] is h(),[3] is f()
       self.openlist.append(cur_point)
       #min_point trace the point with minimal f()
       self.min_point=cur_point

   def AddOpen(self, pre_point, expanded_point):
       #calculate f()=g()+h()
       g=pre_point[1]+self.cost
       h=abs(expanded_point[0]-self.end[0])+abs(expanded_point[1]-self.end[1])
       f=g+h
       cur_point=[expanded_point]+[g]+[h]+[f]
       #if the expanded point is in open list, do not add the point to open list
       #if the cost of expanded point is less than the point in open list, replace it.
       for i in range(len(self.openlist)):
           if self.openlist[i][0]==expanded_point:
               if f<self.openlist[i][3]:
                   self.openlist[i]=cur_point
               return
       #if the expanded point is not in open list, add it
       self.openlist.append(cur_point)

   def AddClose(self, blocks):
       #add any block, which is not in close list, to close list
       for point in blocks:
           if point not in self.closelist:
               self.closelist.append(point)

   def RemovePoint(self, point):
       #add the point to close list
       self.AddClose([point[0]])
       #remove the point from open list
       self.openlist.remove(point)
       #if there is element in the list
       if self.openlist!=[]:
           #update min_point
           self.min_point=[[0,0]]+[0]+[3*self.size]+[3*self.size]
           for each_point in self.openlist:
               if each_point[2]<=self.min_point[2] and each_point[3]<=self.min_point[3]:
                   self.min_point=each_point

   #only do search once, and return the point searched
   def oneSearch(self):
       if self.findpath:
           return "find path"
       elif self.openlist==[]:
           return "no path"
       else:
           if self.min_point[0]==self.end:
               self.findpath=True
               return self.min_point[0]
           else:
               expanded_point=self.min_point[0]
           direct4=[[0,-1],[0,1],[-1,0],[1,0]]#up,down,left,right
           #add available points to open list,up,down,left,right
           for direction in direct4:
               point_x=self.min_point[0][0]+direction[0]
               point_y=self.min_point[0][1]+direction[1]
               if point_x>=0 and point_x<self.size and point_y>=0 and point_y<self.size:
                   point=[point_x,point_y]
                   if point not in self.closelist:
                       self.AddOpen(self.min_point, point)
           #remove the point
           self.RemovePoint(self.min_point)
           return expanded_point
