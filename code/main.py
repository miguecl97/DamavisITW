from queue import PriorityQueue
import sys
from rod import Rod


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
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)

    #reverse the path since we start from (0,0) cell
    total_path.reverse()

    return total_path



def computeRod(cell,orientation,map):
    """Computes a rod based on his middle cell and the orientation 0-> horizontal, 1-> vertical. Returns a rod object if 
    it is possible to create a 1x3 rod with these parameters"""
    numRows=len(map)
    numCols=len(map[0])

    if orientation==0:
       if cell[1]-1>=0 and map[cell[0]][cell[1]-1]!='#' and cell[1]+1<numCols and map[cell[0]][cell[1]+1]!='#':
            left=(cell[0],cell[1]-1)
            right=(cell[0],cell[1]+1)
            return Rod(0,[left,cell,right])

    if orientation==1:
       if cell[0]-1>=0 and map[cell[0]-1][cell[1]]!='#' and cell[0]+1<numRows and map[cell[0]+1][cell[1]]!='#':
            top=(cell[0]-1,cell[1])
            bottom=(cell[0]+1,cell[1])
            return Rod(1,[top,cell,bottom])
    
    return -1



#Based on pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
def aStar(map, start, goal):
    """Performs A* algorithm and computes the minimal path from starting rod to goal rod"""
    numRows=len(map)
    numCols=len(map[0])
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # We use a PriorityQueue to have O(log(N)) efficiency while sorting
    openSet= PriorityQueue()
    cameFrom={} #to create the path
    rods=[] #this is used to create local copy of rods and their g and f values


    #we compute all possible rods of our labyrithn
    for i in range(numRows):
        for j in range(numCols):
            rod0=computeRod((i,j),0,map)
            rod1=computeRod((i,j),1,map)
            if rod0!=-1 : rods.append(rod0)#, print("generando rod", rod0 )
            if rod1!=-1 : rods.append(rod1)#, print("generando rod", rod1 )

    #g is the cost from start to current node max 9999999 movements as for now
    #f is cost from current cell to the goal f=g + h; max 99999999
    for r in rods:
        r.g=999999999#float('inf') pending testing
        r.f=999999999#float('inf')

    #g cost of initial rod is 0
    start.g=0

    #f=g + h
    #f cost for initial rod is h
    start.f=start.h(goal)

    #we initialize the openSet with the first node and its fScore
    openSet.put((start.f,start))

    while not openSet.empty():
        
        current = openSet.get()[1] ## we get the node with lowest fScore
        
        #check if we reached the goal and stop there
        if current.cells==goal.cells and current.orientation==goal.orientation:
            return reconstructPath(cameFrom, current)
        
        neighbors=current.computeNeighbors(map)
        for n in neighbors:

            #better if we use a dictionary, this is a momentary workaround to keep track of g and f
            for r in rods:
                if n.cells==r.cells and n.orientation==r.orientation:
                    n.g=r.g
            # tentative_gScore is the distance from start to the neighbor (1 movement)      
            tentative_gScore=current.g+1
           
            if tentative_gScore < n.g:
                #this path is better than the previosu one, keep it
                cameFrom[n] = current
                n.g = tentative_gScore
                n.f = tentative_gScore + n.h(goal)

                #update g and f for this neighbor in our dictionary
                for r in rods:
                    if current.cells==r.cells and n.orientation==current.orientation:
                        r.g=n.g
                        r.f=n.f
                
                #check if n is in openSet and if not, we add it
                exists=False
                for item in openSet.queue:
                    if item[1].cells==n.cells and item[1].orientation==n.orientation:
                        exists=True
                if not exists:
                    openSet.put((n.f,n))

    #return empty path if there isn't any
    return []



def computeDestination(map):
    """Computes the destination/final rod, tries to create one per each orientation"""
    if computeRod((len(labyrinth)-2,len(labyrinth[0])-1),1,map).cells[0] != (0,0):
        return computeRod((len(labyrinth)-2,len(labyrinth[0])-1),1,map)
    elif computeRod((len(labyrinth)-1,len(labyrinth[0])-2),0,map).cells[0] != (0,0):
        return computeRod((len(labyrinth)-1,len(labyrinth[0])-2),0,map)
    else:   
        return print("Destination rod couldn't be computed")
    
    

if __name__=='__main__':
    #read file with labyrinth
    labyrinth=readLabyrinth(sys.argv[1])

    print("Labyrinth: ")
    for r in labyrinth:
        print(r)

    initialRod=Rod(0,[(0,0),(0,1),(0,2)])
    #print("Initial rod is in cells: ", initialRod.cells, "with orientation ", initialRod.orientation)
    
    destinationRod=computeDestination(labyrinth)
    #print("Destination rod is in cells: ", destinationRod.cells, "with orientation ", destinationRod.orientation)

    #print("Starting A* algorithm")
    path=aStar(labyrinth,initialRod,destinationRod)

    #print("Final path of rods:")
    #for r in path:
        #print(r)
    if len(path)==0: solution=-1
    else:
        solution = len(path)

    print("Result:", solution)
