#https://github.com/MAN1986/pyamaze/blob/main/Demos/A-Star/aStar.py#L50
#https://www.w3schools.com/python/python_lists_methods.asp

from queue import PriorityQueue

def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)

def aStar(m):
    start=(len(m)-1,len(m[0])-1)
    g_score = list()
    f_score = list()
    for i in range(len(m)):
      for j in range(len(m[0])):
          g_score.append((i,j))
          f_score.append((i,j))
          
    #g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    #f_score=[tuple(ele) for ele in m]#{cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(0,0))

    open=PriorityQueue()
    open.put((h(start,(0,0)),h(start,(0,0)),start)) 
    aPath={}
    solution = False
    while not open.empty() & solution==False:
        currCell=open.get()[2]
        if currCell==(1,1):
            solution=True
            break
        for d in 'RA':
            #if se puede rotar for d in 'NSEO'

            #if no se puede rotar then A
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(childCell,(1,1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath

'''
def aStar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(1,1))

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    while not open.empty():
        currCell=open.get()[2]
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(childCell,(1,1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath
''' 

if __name__=='__main__':
    labyrinth = [[".",".",".",".",".",".",".",".","."],
                 ["#",".",".",".","#",".",".",".","."],
                 [".",".",".",".","#",".",".",".","."],
                 [".","#",".",".",".",".",".","#","."],
                 [".","#",".",".",".",".",".","#","."]]
    
    path=aStar(labyrinth)

    solution = path.length