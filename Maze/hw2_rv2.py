#Elements of AI-HW2-q3-rv2.py
import heapq
#create new cell
class Cell(object):
    #initial new cell
    def __init__(self, x,y,reachable):
        
        self.x=x
        self.y=y
        self.reachable=reachable
        self.parent=None
        self.g=0
        self.h=0
        self.f=0
#A star search object        
class MyAStar(object):
    def __init__(self,width,height,walls,start,end):
        #open list
        self.opened=[]
        heapq.heapify(self.opened)
        #close list is visited cells list
        self.closed=set()
        self.cells=[]
        self.grid_height=width
        self.grid_width=height
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x,y) in walls:
                    reachable=False
                else:
                    reachable=True
                self.cells.append(Cell(x,y,reachable))
        self.start=self.get_cell(start[0],start[1])
        self.end=self.get_cell(end[0],end[1])
        
        
    def get_cell(self,x,y):
        return self.cells[x * self.grid_height+y]

       

    
    def get_adjacent_cells(self,cell):
        cells=[]
        if cell.x<self.grid_width-1:
            cells.append(self.get_cell(cell.x+1,cell.y))
        if cell.y>0:
            cells.append(self.get_cell(cell.x,cell.y-1))
        if cell.x>0:
            cells.append(self.get_cell(cell.x-1,cell.y))
        if cell.y<self.grid_height-1:
            cells.append(self.get_cell(cell.x,cell.y+1))
        return cells
    def get_path(self):
        cell=self.end
        path=[(cell.x,cell.y)]
        while cell.parent is not self.start:
            cell=cell.parent
            path.append((cell.x,cell.y))
        path.append((self.start.x,self.start.y))
        path.reverse()
        return path
    def get_heuristic(self,cell):
        #heuristic function is mahattan distance
        return 10*(abs(cell.x-self.end.x)+abs(cell.y-self.end.y))
    
    def update_cell(self,adj,cell):
        adj.g=cell.g+10
        adj.h=self.get_heuristic(adj)
        adj.parent=cell
        adj.f=adj.h+adj.g
    def display_path(self):
        cell=self.end
        while cell.parent is not self.start:
            cell=cell.parent
            print ('path:cell:',(cell.x,cell.y))
    def process(self):
        heapq.heappush(self.opened,(self.start.f,0,self.start))
        n=1
        while len(self.opened):
            f,m,cell=heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is self.end:
                return self.get_path()           
            adj_cells=self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if(adj_cell.f,adj_cell) in self.opened:
                        if adj_cell.g > cell.g+10:
                            self.update_cell(adj_cell,cell)
                    else:
                        self.update_cell(adj_cell,cell)
                        n+=1
                        heapq.heappush(self.opened,(adj_cell.f,n,adj_cell))
                        
#print movement instructions such as step or rotation                        
class Path_Navigate(object):

    def __init__(self,path,facing):
        self.path = path
        self.facing = facing

    def navigate(self):
        for i in range(len(self.path)-1):
            print ("step to:",self.path[i],"facing to: ",self.facing)
            x=self.path[i+1][0]-self.path[i][0]
            y=self.path[i+1][1]-self.path[i][1]
            if self.facing=='N':
                if x==1:
                    print("rotate+90")
                    self.facing='E'
                elif x==-1:
                    print("rotate-90")
                    self.facing='W'
                elif y==-1:
                    print("rotate+90")
                    print("rotate+90")
                    self.facing='S'
            elif self.facing=='E':
                if y==1:
                    print("rotate-90")
                    self.facing='N'
                elif y==-1:
                    print("rotate+90")
                    self.facing='S'
                elif x==-1:
                    print("rotate+90")
                    print("rotate+90")
                    self.facing='W'               
            elif self.facing=='S':
                if x==1:
                    print("rotate-90")
                    self.facing='E'
                elif x==-1:
                    print("rotate+90")
                    self.facing='W'
                elif y==-1:
                    print("rotate+90")
                    print("rotate+90")
                    self.facing='N'
            elif self.facing=='W':
                if y==1:
                    print("rotate+90")
                    self.facing='N'
                elif y==-1:
                    print("rotate-90")
                    self.facing='S'
                elif x==1:
                    print("rotate+90")
                    print("rotate+90")
                    self.facing='E'
        print ("move to:",self.path[i+1],"facing to: ",self.facing)
#maze object        
class MyMaze(object):
    
    def __init__(self,filename):
        mazeFile = open(filename, "r")
        self.maze=[]
        self.walls=[]
        columns = mazeFile.readlines()
        for column in columns:
            column = column.strip()
            row = [i for i in column]
            self.maze.append(row)
        self.width=len(columns)
        self.height=len(row)
        for k in range(self.width):
            for j in range(self.height):
                if self.maze[j][k]=='1':
                    self.walls.append((k,self.height-1-j))

#main function
mymaze=MyMaze("f.txt")
walls=mymaze.walls                    
width=mymaze.width
height=mymaze.height
start=[2,0]
end=[0,4]
myastar=MyAStar(width,height,walls,start,end)
finalpath=myastar.process()

if finalpath:
    print("Here it is the shortest path by A* search:")
    Path_Navigate(finalpath,'N').navigate()
else:
    print("no path found")
