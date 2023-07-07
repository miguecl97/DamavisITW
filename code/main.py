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



def computeRod(cell,orientation,map):
    numRows=len(map)
    numCols=len(map[0])

    if orientation==0:
       if cell[1]-1>=0 and cell[1]+1<numCols:
            left=(cell[0],cell[1]-1)
            right=(cell[0],cell[1]+1)
            return [left,cell,right]

    if orientation==1:
       if cell[0]-1>=0 and cell[0]+1<numRows:
            top=(cell[0]-1,cell[1])
            bottom=(cell[0]+1,cell[1])
            return [top,cell,bottom]
    
    return[]



###not used care.
def d(cell1,cell2):
    """This function computes the Mahattan distance,is a distance measure that is calculated by taking the sum of distances between the x and y coordinates."""
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)


def h(rod1,rod2):
    """This function computes the Mahattan distance,is a distance measure that is calculated by taking the sum of distances between the x and y coordinates."""
    #x2,y2=cell2

    #rod1=computeRod(cell1)
    #rod2=computeRod(cell2)
   
    distance=0

    for i in range(len(rod1)):
        distance+=abs(rod1[i][1]-rod2[i][1]) + abs(rod1[i][2]-rod2[i][2])

    return distance


def computeNeighbors(map,cell,orientation):
    """Computes all the possible neighbors given a static cell"""
    numRows=len(map)
    numCols=len(map[0])

    rod=computeRod(cell,orientation,map)
    neighbors=[]

    for m in 'RNSWE':
        newRod=[]
        if m=='R':
          if orientation==0:
            if rod[1][1]+1<numCols and rod[1][0]-1<numRows and map[rod[1][0]-1,rod[1][1]+1]!='#':
                if rod[2][1]-1<numCols and rod[2][0]+1<numRows and map[rod[2][0]+1,rod[2][1]-1]!='#':
                   neighbors().append([(rod[1][0]-1,rod[1][1]+1),(cell),(rod[2][0]+1, rod[2][1]-1)])               
          if orientation==1:
             if rod[1][1]-1<numCols and rod[1][0]+1<numRows and map[rod[1][0]+1,rod[1][1]-1]!='#':
                if rod[2][1]+1<numCols and rod[2][0]-1<numRows and map[rod[2][0]-1,rod[2][1]+1]!='#':
                   neighbors().append([(rod[1][0]+1,rod[1][1]-1),(cell),(rod[2][0]-1,rod[2][1]+1)])
      
        if m=='N':
          valid=True
          for c in rod:
             newRod.append(c)
             if not c[0]-1>=0 and map[c[0]-1][c[1]]!='#':
                valid=False
          if valid:
            neighbors().append(newRod)

        if m=='S':
          valid=True
          for c in rod:
             newRod.append(c)
             if not c[0]+1<numRows and map[c[0]+1][c[1]]!='#':
                valid=False
          if valid:
            neighbors().append(newRod)

        if m=='W':
          valid=True
          for c in rod:
             newRod.append(c)
             if not c[1]-1>=0 and map[c[0]][c[1]-1]!='#':
                valid=False
          if valid:
            neighbors().append(newRod)

        if m=='E':
          valid=True
          for c in rod:
             newRod.append(c)
             if not c[1]+1<numCols and map[c[0]][c[1]+1]!='#':
                valid=False
          if valid:
            neighbors().append(newRod)

    return neighbors


#Based on pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def aStar(map, start, goal):
    """Performs A* algorithm and computes the minimal path from starting cell to goal cell"""
    numRows=len(map)
    numCols=len(map[0])
    openSet= PriorityQueue()
    cameFrom={}
    grid=[]
    rods=[]

    for i in range(numRows):
        for j in range(numCols):
            rods.append(computeRod((i,j),0,map))
            rods.append(computeRod((i,j),1,map))

    #g is the cost from start to current node
    #print(map)
    #print(grid)
    gScore={rod:float('inf') for rod in rods} ##cost to reach current cell
    gScore[(start)]=0

    #f=g + h
    fScore={rod:float('inf') for rod in rods} ##cost from current cell to the goal might be 1000 max
    fScore[(start)]=h(start,goal)

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

def computeDestination(map):
   lastCell=(len(labyrinth)-1,len(labyrinth[0])-1)
   for i in range(1):
      if len(computeRod(lastCell,i,map)) != 0:
        return computeRod(lastCell,i,map)
    

if __name__=='__main__':
    #labyrinth=readLabyrinth(sys.argv[1])

    labyrinth = [[".",".",".",".",".",".",".",".","."],
                 ["#",".",".",".","#",".",".",".","."],
                 [".",".",".",".","#",".",".",".","."],
                 [".","#",".",".",".",".",".","#","."],
                 [".","#",".",".",".",".",".","#","."]]
    
    initialRod=[(0,0),(0,1),(0,2)]
    destinationRod=computeDestination(labyrinth)
    path=aStar(labyrinth,initialRod,destinationRod)

    print("camino final", path)

    solution = len(path)

