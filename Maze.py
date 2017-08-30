import random
import sys
sys.setrecursionlimit(20000)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

def maze_init(size):
    maze = []
    for x in range(size):
        row = []
        for y in range(size):
           row.append("#")
        maze.append(row)
    return maze

size = 11
maze = maze_init(size)

def can_destroy(row, col):
    return row > 0 and col > 0 and row < len(maze)-1 and col < len(maze)-1 and maze[row][col] == "#"

def rand_direction(row, col):
    directions = []
    length = 0
    if can_destroy(row, col+2):
        directions.append(EAST)
        length+=1
    if can_destroy(row+2, col):
        directions.append(SOUTH)
        length+=1
    if can_destroy(row, col-2):
        directions.append(WEST)
        length+=1
    if can_destroy(row-2, col):
        directions.append(NORTH)
        length+=1
    if length == 0:
        return -1
    else:
        return directions[random.randint(0, length-1)]

def destroy(row, col, dir):
    if dir == NORTH:
        maze[row-1][col] = maze[row-2][col] = " "
    elif dir == EAST:
        maze[row][col+1] = maze[row][col+2] = " "
    elif dir == SOUTH:
        maze[row+1][col] = maze[row+2][col] = " "
    elif dir == WEST:
        maze[row][col-1] = maze[row][col-2] = " "

def get_loc(row, col, dir):
    if dir == NORTH:
         return Location(row-2, col)
    elif dir == EAST:
        return Location(row, col+2)
    elif dir == SOUTH:
        return Location(row+2, col)
    elif dir == WEST:
        return Location(row, col-2)

def print_maze():
	for x in range(len(maze)):
		for y in range(len(maze)):
			print(maze[x][y], end="")
		print("")

def generate(row, col): #creates the paths
    con = True
    while(con):
        dir = rand_direction(row, col)
        if dir == -1:
            con = False
            break
        else:
            destroy(row, col, dir)
            loc = get_loc(row, col, dir)
            generate(loc.row, loc.col)

def find_dead_end():
	dead_ends = []
	count = 0
	for x in range(1, len(maze)-2):
		for y in range(1, len(maze)-2):
			if maze[x][y] == " ":
				if maze[x-1][y] == "#":
					count+=1
				if maze[x][y+1] == "#":
					count+=1
				if maze[x][y-1] == "#":
					count+=1
				if maze[x+1][y] == "#":
					count+=1
			if count >= 3:
				dead_ends.append(Location(x, y))
			count = 0
	return dead_ends[random.randint(0, len(dead_ends)-1)]
					
				


go = True
while go:
    #size = int(input("Enter a size: ")) #size can't be too big otherwise it reaches max recursion depth
    size = 35
    if size <= 0 or type(size) != int: #odd number sizes look nicer
        go = False
    else:
        maze = maze_init(size)
        maze[-1][1] = "$"
        generate(len(maze)-2, 1)
        ending = find_dead_end();
        maze[ending.row][ending.col] = "@"
        print_maze()
        print("")

