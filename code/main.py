#https://github.com/MAN1986/pyamaze/blob/main/Demos/A-Star/aStar.py#L50
#https://www.w3schools.com/python/python_lists_methods.asp

from queue import PriorityQueue


def reconstructPath(cameFrom, current):
    total_path= {current}
    while current in cameFrom.keys:
        current = cameFrom[current]
        total_path.append(current)###might be prepend
    
    return total_path



#distancia Manhattan
def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)



def computeNeighbors(map,current):
    numRows=len(map)
    numCols=len(map[0])

    neighbors={}
    i=current[0]
    j=current[1]

    for m in 'NSWE':
        if m=='N':
          if i-1>=0 & map[i-1][j]!='#':
            neighbors.append(i-1,j)
        if m=='S':
          if i+1<numRows & map[i+1][j]!='#':
            neighbors.append(i+1,j)
        if m=='W':
          if i-1>=0 & map[i][j-1]!='#':
            neighbors.append(i,j-1)
        if m=='E':
          if j+1<numCols & map[i][j+1]!='#':
            neighbors.append(i,j+1)

    return neighbors


#A star algorithm https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def aStar(map, start, goal):
    numRows=len(map)
    numCols=len(map[0])

    openSet= PriorityQueue()

    cameFrom={}

    grid=[]
    for i in range(numRows):
        for j in range(numCols):
            grid.append(i,j)

    gScore={cell:float('inf') for cell in grid} ##cost to reach current cell
    gScore[start]=0

    #might be 1000 max
    fScore={cell:float('inf') for cell in grid} ##cost from current cell to the goal might be 1000 max
    fScore[start]=h(start,goal)

    openSet.put(fScore[start],start)
    while not openSet.empty():
        current = openSet.get()[2] ## we get the node with lowest fScore

        if current==goal:
            return reconstructPath(cameFrom, current)
        
        openSet.remove(fScore[current],current)
        neighbors=computeNeighbors(map,current)

        for n in neighbors:
            tentative_gScore=gScore[current]+h(current,n)
            if tentative_gScore<gScore[n]:
                cameFrom[n]=current
                gScore[n]=tentative_gScore
                fScore[n]= tentative_gScore + h(n,goal)
            if not openSet.contains(fScore[n],n): 
                openSet.add(fScore[n],n)

    return []



if __name__=='__main__':
    labyrinth = [[".","#","#"],
                [".","#","."],
                [".",".","."]]
    path=aStar(labyrinth,(0,0),(len(labyrinth)-1,len(labyrinth[0])-1))
    solution = len(path)

'''    labyrinth = [[".",".",".",".",".",".",".",".","."],
                 ["#",".",".",".","#",".",".",".","."],
                 [".",".",".",".","#",".",".",".","."],
                 [".","#",".",".",".",".",".","#","."],
                 [".","#",".",".",".",".",".","#","."]]''' 