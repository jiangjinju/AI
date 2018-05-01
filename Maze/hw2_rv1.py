#Elements of AI-HW2-q3-rv1.py
class MyStack(object):
    #define stack data structure
    def __init__(self):
        self.stack = []

    def empty(self):
        return self.stack == []

    def pop(self):
        if self.empty():
            return None
        else:
            item = self.stack.pop()
            return item

    def push(self, item):
        self.stack.append(item)

class Cell(object):
    #initial new cell
    def __init__(self, x,y,reachable):
        
        self.x=x
        self.y=y
        self.reachable=reachable
        self.parent=None
        
class MyDFS(object):
    def __init__(self,width,height,walls,start,end):
        #open list
        self.opened=MyStack()
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

    def update_cell(self,adj,cell):
        adj.parent=cell 

    
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
   
    def process(self):
        self.opened.push(self.start)
        while not self.opened.empty():
            cell=self.opened.pop()
            self.closed.add(cell)
            if cell is self.end:
                return self.get_path()
                break
            adj_cells=self.get_adjacent_cells(cell)

            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                        self.update_cell(adj_cell,cell)
                        self.opened.push(adj_cell)
            if self.opened.empty():
                return None
        
                        
class Path_Navigate(object):

    def __init__(self,path,facing):
        self.path = path
        self.facing = facing

    def navigate(self):
        for i in range(len(self.path)-1):
            print ("move to:",self.path[i],"facing to: ",self.facing)
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

#load maze file
mymaze=MyMaze("f.txt")
walls=mymaze.walls                    
width=mymaze.width
height=mymaze.height
start=[2,0]
end=[0,4]
mydfs=MyDFS(width,height,walls,start,end)
finalpath=mydfs.process()
#if there is path, then print the instructions
if finalpath:
    print("Here it is the shortest path by DFS search:")
    Path_Navigate(finalpath,'N').navigate()
#otherwise print no path found
else:
    print("no path found")