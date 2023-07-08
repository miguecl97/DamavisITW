class Rod:
    """class rod which is an 1x3 object in a labyrinth with an orientation, it also has a gScore and fScore"""
    def __init__(self, orientation=0, cells=[(0,0),(0,1),(0,2)], g=0, f=0):
        self.cells = cells
        self.orientation = orientation
        self.g=g
        self.f=f


    def h(self,rod2):
        """This function computes the euclidean distance,is a distance measure that is calculated by taking the sum of distances between the x and y coordinates."""
        distance=0
        #in this case as each rod has 3 coordinates, we calculate the distance coordinate per coordinate
        for i in range(len(self.cells)):
            distance+=abs(self.cells[i][0]-rod2.cells[i][0]) + abs(self.cells[i][1]-rod2.cells[i][1])

        return distance

    def computeNeighbors(self,map):
        """Computes all the possible neighbors given a static cell"""
        numRows=len(map)
        numCols=len(map[0])

        neighbors=[]

        #there are 5 possible moves for a rod 
        # R->Rotate 90 degres using center cell as an edge
        # N-> move up
        # S-> move down
        # W-> move left
        # E-> move right
        for m in 'RNSWE':
            newRod=[]
            valid=True
            if m=='R':
                if self.orientation==0:
                    ###check if we have enough space to rotate 
                    if self.cells[0][1]+1<numCols and self.cells[0][0]-1>=0 and map[self.cells[0][0]-1][self.cells[0][1]+1]!='#':
                        if self.cells[2][1]-1<numCols and self.cells[2][0]+1<numRows and map[self.cells[2][0]+1][self.cells[2][1]-1]!='#':
                            neighbors.append(Rod(1,[(self.cells[0][0]-1,self.cells[0][1]+1),self.cells[1],(self.cells[2][0]+1, self.cells[2][1]-1)],self.g,self.f))               
                    #check if we have enough space to rotate
                if self.orientation==1:
                    if self.cells[0][1]-1<=0 and self.cells[0][0]+1<numRows and map[self.cells[0][0]+1][self.cells[0][1]-1]!='#':
                        if self.cells[2][1]+1<numCols and self.cells[2][0]-1<numRows and map[self.cells[2][0]-1][self.cells[2][1]+1]!='#':
                            neighbors.append(Rod(0,[(self.cells[0][0]+1,self.cells[0][1]-1),self.cells[1],(self.cells[2][0]-1,self.cells[2][1]+1)],self.g,self.f))
        
            if m=='N':
                #check if we can move up
                for c in self.cells:
                    newRod.append((c[0]-1,c[1]))
                    if not (c[0]-1>=0 and map[c[0]-1][c[1]]!='#'):
                        valid=False
                if valid:
                    neighbors.append(Rod(self.orientation,newRod,self.g,self.f))

            if m=='S':
                #check if we can move down
                for c in self.cells:
                    newRod.append((c[0]+1,c[1]))
                    if not (c[0]+1<numRows and map[c[0]+1][c[1]]!='#'):
                        valid=False
                if valid:
                    neighbors.append(Rod(self.orientation,newRod,self.g,self.f))

            if m=='W':
                #check if we can move left
                for c in self.cells:
                    newRod.append((c[0],c[1]-1))
                    if not (c[1]-1>=0 and map[c[0]][c[1]-1]!='#'):
                        valid=False
                if valid:
                    neighbors.append(Rod(self.orientation,newRod,self.g,self.f))

            if m=='E':
                #check if we can move right
                valid=True
                for c in self.cells:
                    newRod.append((c[0],c[1]+1))
                    if not (c[1]+1<numCols and map[c[0]][c[1]+1]!='#'):
                        valid=False
                if valid:
                    neighbors.append(Rod(self.orientation,newRod,self.g,self.f))

        return neighbors
    
    #ToDo: compare 2 rods to check which is best to pick
    def __lt__(self, other):
        if self.cells[1][0]>=other.cells[1][0] and self.cells[1][1]>=other.cells[1][1]:
            return True
        else:
            return False

        
    def __str__(self):
        """prints a rod (for debuggin purposes mostly)"""
        return f"Cells: {self.cells}, orientation: {self.orientation}"