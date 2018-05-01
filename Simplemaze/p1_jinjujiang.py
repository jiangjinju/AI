#Elements of AI_Hw1_The Drone Scanning Room Python Script     
def find_shortest_path(graph, start, end, path=[]): # for return path
        path = path + [start]
        if start == end:
            return path
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

def dfs_iterative(graph, start): #DFS to scan all rooms, the output is the sequence of room scanned
    stack, path = [start], []
    start1=start
    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        path.append(vertex)
        for neighbor in graph[vertex]:
            stack.append(neighbor)
    return path
# use python data structure to define graph
graph = {'A': set(['B']),
         'B': set(['A', 'H', 'J']),
         'C': set(['I', 'U']),
         'D': set(['F', 'K', 'L']),
         'E': set(['F']),
         'F': set(['D', 'E']),
         'G': set(['H', 'J', 'K']),
         'H': set(['B', 'G']),
         'I': set(['C']),
         'J': set(['B', 'G']),
         'K': set(['D', 'G']),
         'L': set(['D', 'U']),
         'U': set(['C', 'L'])}
items=dfs_iterative(graph,'U') # the start point is U
items.append('U') #append U to make sure the end point is U
totaltime=0 #total time including scanning time, back and forth move time
batteryqty=1 #initially there is one batter in the drone
batterylife=0 #currently battery used
for index in range(len(items)-1):
    if batterylife>35:
        print("Warning! Please change your battery: ",45-batterylife, "mins left")
        batteryqty +=1
        batterylife=0
        print("Congratulations!",batteryqty,"th New Battery is loaded successfully")
    scanandmovetime=6
    if items[index]=='U':
        scanandmovetime=0
    totaltime +=scanandmovetime
    batterylife +=scanandmovetime
    if batterylife>35:
        print("Warning! Please change your battery: ",45-batterylife, "mins left")
        batteryqty +=1
        batterylife=0
        print("Congratulations!",batteryqty,"th New Battery is loaded successfully")
    print(index, "scan room:",items[index],"scan&movetime: ",scanandmovetime,"Accumulatetime:",totaltime)
    if items[index] not in graph[items[index+1]]:
        returnpath=find_shortest_path(graph,items[index],items[index+1])
        movetime=2*(len(returnpath)-2)
        if 'U' in returnpath:
            if returnpath.index('U') in range(0,len(returnpath)-1) :
                movetime=2*(len(returnpath)-3)+7
        totaltime +=movetime
        batterylife +=movetime
        if batterylife>35:
            print("Warning! Please change your battery: ",45-batterylife)
            batteryqty +=1
            batterylife=0
            print("Congratulations!",batteryqty,"th New Battery is loaded successfully")
        print("Returnpath: ",returnpath,"movetime:",movetime,"Accumulatetime:",totaltime)
totaltime +=2*2 #for last return path moving time, we need to add 2*2
batterylife +=2*2
if batterylife>35:
    print("Warning! Please change your battery: ",45-batterylife, "mins left")
    batteryqty +=1
    batterylife=0
    print("Congratulations!",batteryqty,"th New Battery is loaded successfully")
print("Totaltime: ",totaltime)
print("Batteryused:", batteryqty)
print(45-batterylife,"mins battery left")