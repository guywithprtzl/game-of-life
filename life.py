from tkinter import *
grid = []
m = 25

def main():
#MAIN
    get_in()
    initialise()
    mainloop()

def initialise():
    build_graph()

def build_graph():
    global graph
    global m
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
    newGrid = next_gen()
    graph.delete(ALL)
    row = 0
    while row < len(newGrid):
        col = 0
        while col < len(newGrid[0]):
            cell = newGrid[row][col]
            startX = m*col
            endX = startX+m
            startY = m*row
            endY = startY+m
            if cell == 1:
                graph.create_rectangle(startX,startY,endX,endY,fill="red")
            else:
                graph.create_rectangle(startX,startY,endX,endY,fill="black")
            col = col+1
        row = row+1
    graph.update()
