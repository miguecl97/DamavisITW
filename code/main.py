#https://github.com/MAN1986/pyamaze/blob/main/Demos/A-Star/aStar.py#L50
#https://www.w3schools.com/python/python_lists_methods.asp

from queue import PriorityQueue
import sys
 

def readLabyrinth(filename):
    """A simple function that reads a file with the entry format required by the PDF shared, it returns a maze"""
    labyrithnFile = open(filename, "r")
    rows = labyrithnFile.readlines()
    i=0
    labyrinth=[[]]
    #this for loop iterates every row of the file, adds a new array per row and adds the characters to the array
    for row in rows:
        if i!=0: labyrinth.append([])
        for char in row:
           if char =='#' or char=='.':
              labyrinth[i].append(char)
        i+=1
    return labyrinth




def reconstructPath(cameFrom, current):
    """This function iterates a path of cells using a dictionary with the format cell->child"""
    total_path=[current]
    print("camefrom", cameFrom)
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)

    #reverse the path since we start from (0,0) cell
    total_path.reverse()

    return total_path



def h(cell1,cell2):
    """This function computes the Mahattan distance,is a distance measure that is calculated by taking the sum of distances between the x and y coordinates."""
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)



def computeNeighbors(map,current):
    """Computes all the possible neighbors given a static cell"""
    numRows=len(map)
    numCols=len(map[0])

    neighbors=[]
    i=current[0]
    j=current[1]

    #current moves are N=move up; S=move down;  W=move left; E=move right
    for m in 'NSWE':
        if m=='N':
          if i-1>=0 and map[i-1][j]!='#':
            neighbors.append((i-1,j))
        if m=='S':
          if i+1<numRows and map[i+1][j]!='#':
            neighbors.append((i+1,j))
        if m=='W':
          if j-1>=0 and map[i][j-1]!='#':
            neighbors.append((i,j-1))
        if m=='E':
          if j+1<numCols and map[i][j+1]!='#':
            neighbors.append((i,j+1))

    return neighbors


#Based on pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def aStar(map, start, goal):
    """Performs A* algorithm and computes the minimal path from starting cell to goal cell"""
    numRows=len(map)
    numCols=len(map[0])
    openSet= PriorityQueue()
    cameFrom={}
    grid=[]

    for i in range(numRows):
        for j in range(numCols):
            grid.append((i,j))

    #g is the cost from start to current node
    #print(map)
    #print(grid)

    gScore={cell:float('inf') for cell in grid} ##cost to reach current cell
    gScore[start]=0

    #f=g + h
    fScore={cell:float('inf') for cell in grid} ##cost from current cell to the goal might be 1000 max
    fScore[start]=h(start,goal)

    openSet.put((fScore[start],start))
    #print(openSet.get()[1])
    while not openSet.empty():
        current = openSet.get()[1] ## we get the node with lowest fScore
        
        if current==goal:
            return reconstructPath(cameFrom, current)
        
        neighbors=computeNeighbors(map,current)
        #print("vecinos de", current, ": ", neighbors)
        #print("----------\n")
        for n in neighbors:
            #print("explorando vecino", n, "gScore[current]=", gScore[current] )
            tentative_gScore=gScore[current]+1
            #print("tentativegScore: ", tentative_gScore, "gScoreN", gScore[n])
            if tentative_gScore < gScore[n]:
                cameFrom[n] = current
                gScore[n] = tentative_gScore
                fScore[n] = tentative_gScore + h(n,goal)
                if not any((n in item[1] for item in openSet.queue)):
                    openSet.put((fScore[n],n))

    return []



if __name__=='__main__':
    labyrinth=readLabyrinth(sys.argv[1])
    print(labyrinth)
    path=aStar(labyrinth,(0,0),(len(labyrinth)-1,len(labyrinth[0])-1))

    print("camino final", path)

    solution = len(path)

'''    labyrinth = [[".",".",".",".",".",".",".",".","."],
                 ["#",".",".",".","#",".",".",".","."],
                 [".",".",".",".","#",".",".",".","."],
                 [".","#",".",".",".",".",".","#","."],
                 [".","#",".",".",".",".",".","#","."]]''' 