from tkinter import *
grid = [] #where the grid is stored
m = 25
windowWidth = 800
windowHeight = 800
gens = 0
currentGens = 0

def main():
    #MAIN
    getInput()
    initialise()
    mainLoop()

def initialise():
    build_graph()


def build_graph():
    global graph
    global m
    global grid
    WIDTH = m*len(grid[0])
    HEIGHT = m*len(grid)
    root = Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, (root.winfo_screenwidth() - WIDTH) / 2, (root.winfo_screenheight() - HEIGHT) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.after(40, update)
    graph.pack()


def update():
    draw()
    graph.after(500,update)

def draw():
    global m
    global gens
    global currentGens
    global grid
    global graph
    #print("gens: ", gens, " currentGens: ", currentGens)
    if currentGens <= gens and currentGens != 0:
        #print("next")
        newGrid = nextGen()
        #print(newGrid)
    else:
        newGrid = grid
    graph.delete(ALL)
    row = 0
    while row < len(newGrid):
        col = 0
        while col < len(newGrid[0]):
            cell = newGrid[row][col]
            #print(cell)
            startX = m*col
            endX = startX+m
            startY = m*row
            endY = startY+m
            #print("startX:",startX)
            #print("endX:",endX)
            #print("startY:",startY)
            #print("endY:",endY)
            if cell == 1:
                graph.create_rectangle(startX,startY,endX,endY,fill="yellow")
                #print("red")
            elif cell == 0:
                graph.create_rectangle(startX,startY,endX,endY,fill="brown")
            col = col+1
        row = row+1
    currentGens = currentGens + 1
    graph.update()
     

def nextGen():
    global grid
    newGrid = []
    i = 0
    while i < len(grid):
        # setup new grid
        newGrid.append([])
        
        j = 0
        while j < len(grid[0]):
            newGrid[i].append(2)
            j = j + 1
        i = i+1
        
    row = 0
    while row < len(grid):
        col = 0
        while col < len(grid[0]):
            
            cell = grid[row][col]
            newCell = 0
            liveNeighbours = sumLiveNeighbours(row,col)
            
            if cell == 1:
                if liveNeighbours < 2:
                    # dies of lonliness
                    newCell = 0

                elif liveNeighbours > 3 and liveNeighbours < 9:
                    # dies of overcrowding
                    newCell = 0
                    
                elif liveNeighbours > 1 and liveNeighbours < 4:
                    # lives
                    newCell = 1
                
            elif cell == 0:
                if liveNeighbours == 3:
                    # born
                    newCell = 1
                    
                else:
                    # stays dead
                    newCell = 0
                    
            newGrid[row][col] = newCell
            col = col+1
        row = row+1
    grid = newGrid
    return newGrid

def getInput():
    global grid
    gridAsStrings = fileRead("inLife.txt")
    grid = parseGrid(gridAsStrings)
    #print(grid)

def parseGrid(gridAsStrings):
    initialGrid = []
    for line in gridAsStrings:
        splitCells = list(line)
        gridline = []
        for stringCell in splitCells:
            cell = int(stringCell)
            gridline.append(cell)
        initialGrid.append(gridline)
    return initialGrid
    
    
def fileRead(filename):
    global m
    global gens
    gridAsStrings = []
    with open(filename, "r") as f:
        getGen = True
        for line in f:
            if getGen == False:
                gridlineAsString = line.rstrip()
                gridAsStrings.append(gridlineAsString)

            else:
                gensAsString = line.rstrip()
                gens = int(gensAsString)
                getGen = False
    #print(gridAsStrings)
    return gridAsStrings

def sumLiveNeighbours(row, col):
    currentCell = grid[row][col]
    rightMost = len(grid[0])-1
    bottomMost = len(grid)-1
    liveNeighbours = 0
    northWestNeighbour = 0
    northNeighbour = 0
    northEastNeighbour = 0
    eastNeighbour = 0
    southEastNeighbour = 0
    southNeighbour = 0
    southWestNeighbour = 0
    westNeighbour = 0
    if (row == 0 and col == 0):
        # in top left corner of grid
        eastNeighbour = grid[row][col+1]
        southEastNeighbour = grid[row+1][col+1]
        southNeighbour = grid[row+1][col]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour
        
    elif (row == 0 and col == rightMost):
        # in top right corner of grid
        southNeighbour = grid[row+1][col]
        southWestNeighbour = grid[row+1][col-1]
        westNeighbour =  grid[row][col-1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    elif (row == bottomMost and col == 0):
        # in bottom left corner of grid
        northNeighbour = grid[row-1][col]
        northEastNeighbour = grid[row-1][col+1]
        eastNeighbour = grid[row][col+1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    elif (row == bottomMost and col == rightMost):
        # in bottom right corner of grid
        northWestNeighbour = grid[row-1][col-1]
        northNeighbour = grid[row-1][col]
        westNeighbour =  grid[row][col-1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    elif (row == 0 and col != 0 and col != rightMost):
        # in top edge of grid. not a corner1]
        eastNeighbour = grid[row][col+1]
        southEastNeighbour = grid[row+1][col+1]
        southNeighbour = grid[row+1][col]
        southWestNeighbour = grid[row+1][col-1]
        westNeighbour =  grid[row][col-1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    elif (row != 0 and row != bottomMost and col == rightMost):
        # in right edge of grid. not a corner
        northWestNeighbour = grid[row-1][col-1]
        northNeighbour = grid[row-1][col]
        southNeighbour = grid[row+1][col]
        southWestNeighbour = grid[row+1][col-1]
        westNeighbour =  grid[row][col-1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    elif (row == bottomMost and col != 0 and col != rightMost):
        # in bottom edge of grid. not a corner
        northWestNeighbour = grid[row-1][col-1]
        northNeighbour = grid[row-1][col]
        northEastNeighbour = grid[row-1][col+1]
        eastNeighbour = grid[row][col+1]
        westNeighbour =  grid[row][col-1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    elif (row != bottomMost and row != 0 and col == 0):
        # in left edge of grid. not a corner
        northNeighbour = grid[row-1][col]
        northEastNeighbour = grid[row-1][col+1]
        eastNeighbour = grid[row][col+1]
        southEastNeighbour = grid[row+1][col+1]
        southNeighbour = grid[row+1][col]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    else:
        # surrounded by 8 existing neighbours
        northWestNeighbour = grid[row-1][col-1]
        northNeighbour = grid[row-1][col]
        northEastNeighbour = grid[row-1][col+1]
        eastNeighbour = grid[row][col+1]
        southEastNeighbour = grid[row+1][col+1]
        southNeighbour = grid[row+1][col]
        southWestNeighbour = grid[row+1][col-1]
        westNeighbour =  grid[row][col-1]
        liveNeighbours = northWestNeighbour + northNeighbour + northEastNeighbour + eastNeighbour \
                         + southEastNeighbour + southNeighbour + southWestNeighbour + westNeighbour

    return liveNeighbours


def mainLoop():
    
    pass


main()
