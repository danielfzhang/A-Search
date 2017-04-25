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
       #calculate f() + g() + h()
       g=0
       h=abs(self.start[0]-self.end[0])+abs(self.start[1]-self.end[1])
       f=g+h
       cur_point=[start]+[g]+[h]+[f]
       #[0] is index, [1] is g(), [2] is h(),[3] is f()
       self.openlist.append(cur_point)
       #min_point trace the point with minimal f()
       self.min_point=cur_point

   def OpenAdd(self, pre_point, expanded_point):
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

   def CloseAdd(self, blocks):
       #add any block, which is not in close list, to close list
       for point in blocks:
           if point not in self.closelist:
               self.closelist.append(point)

   def PointRemove(self, point):
       #add the point to close list
       self.CloseAdd([point[0]])
       #remove the point from open list
       self.openlist.remove(point)
       # if openlist is empty return "openlist empty"
       if self.openlist==[]:
           return "openlist empty"
       else:
           #update min_point
           self.min_point=[[0,0]]+[0]+[0]+[3*self.size]
           for each_point in self.openlist:
               if each_point[3]<self.min_point[3]:
                   self.min_point=each_point

   #only do search once, and return the point searched
   def oneSearch(self):
       if self.openlist==[]:
           return "openlist empty"
       else:
           #add available points to open list
           #up
           if self.min_point[0][1]-1>=0:
               point=[self.min_point[0][0],self.min_point[0][1]-1]
               if point not in self.closelist:
                   if point==self.end:
                       return "find path"
                   else:
                       self.OpenAdd(self.min_point, point)
           #down
           if self.min_point[0][1]+1<self.size:
               point=[self.min_point[0][0],self.min_point[0][1]+1]
               if point not in self.closelist:
                   if point==self.end:
                       return "find path"
                   else:
                       self.OpenAdd(self.min_point, point)
           #left
           if self.min_point[0][0]-1>=0:
               point=[self.min_point[0][0]-1,self.min_point[0][1]]
               if point not in self.closelist:
                   if point==self.end:
                       return "find path"
                   else:
                       self.OpenAdd(self.min_point, point)
           #right
           if self.min_point[0][0]+1<self.size:
               point=[self.min_point[0][0]+1,self.min_point[0][1]]
               if point not in self.closelist:
                   if point==self.end:
                       return "find path"
                   else:
                       self.OpenAdd(self.min_point, point)
           #remove the point
           self.PointRemove(self.min_point)
           return self.min_point[0]

start=[0,0]
end=[20,20]
blocks1=[]
s=Astar(start,end,blocks1,30,1)
print("close list:", end="")
print(s.closelist)
print("open list:", end="")
print(s.openlist)
print("min point:", end="")
print(s.min_point)
print("---------------------")

while True:
    result=s.oneSearch()
    print(result)
    if result=="find path" or result=="openlist empty":
        break
