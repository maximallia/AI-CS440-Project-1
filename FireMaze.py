from tkinter import *
from random import randint
from matplotlib import pyplot as plt
from datetime import datetime
import heapq
import math

'''
    Kyle VanWageninge kjv48
    Daniel Ying dty16
    AI Project 1 Fire Maze
'''


# Node class for squares in maze
class Node:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.h = 0
        self.numP = 0

    # Can change the parent of the node
    def changeParent(self, new_parent):
        self.parent = new_parent

    # returns the parent of the node
    def getParent(self):
        return self.parent

    # returns the coordinates of the node
    def getCords(self):
        return [self.x, self.y]

    # sets the heuristic of the node (for A*)
    def giveH(self, h):
        self.h = h

    # sets the number of parents the node has
    def addParent(self, x):
        self.numP = x

    # returns the current cost of the node
    def getCost(self):
        return self.numP

    # returns the heuristic of the node
    def getH(self):
        return self.h

    def __lt__(self, other):
        return self.h < other.h


# size of square for maze GUI
cell_size = 30
# dim of maze and p of maze
size = int(sys.argv[1])
p = getdouble(sys.argv[2])

# Initialize the maze with given size
maze = [['w' for _ in range(size)] for _ in range(size)]


# assign each square a color
def create(ffs1, maze1):
    for row in range(size):
        for col in range(size):
            if maze1[row][col] == 'w' or maze1[row][col] == 'c':
                color = 'White'
            elif maze1[row][col] == 'P':
                color = 'black'
            elif maze1[row][col] == 'r':
                color = 'red'
            elif maze1[row][col] == 's':
                color = 'green'
            elif maze1[row][col] == 'g':
                color = 'yellow'
            elif maze1[row][col] == 'x':
                color = 'grey'
            elif maze1[row][col] == 'c':
                color = 'pink'
            elif maze1[row][col] == 'f':
                color = 'red'
            draw(row, col, color, ffs1)


# draw the color of each square to the screen using the cell_size and row col position
def draw(row, col, color, ffs1):
    x1 = col * cell_size
    y1 = row * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size
    ffs1.create_rectangle(x1, y1, x2, y2, fill=color)


# uses the given probability to assign each square a wall or not
def createMaze():
    for row in range(size):
        for col in range(size):
            src = randint(1, 100)
            prob = p * 100
            if src <= prob:
                maze[row][col] = 'P'
    maze[0][0] = 's'
    maze[size - 1][size - 1] = 'g'


# Checks if the move is valid
def canMove(row, col):
    if row < 0 or col < 0:
        return False
    if row >= size or col >= size:
        return False
    if maze_copy[row][col] == 'P' or maze_copy[row][col] == 'c' or maze_copy[row][col] == 's':
        return False
    if maze_copy[row][col] == 'f':
        return False
    if maze_copy[row][col] != 'g':
        maze_copy[row][col] = 'c'
    return True


# finds the number of parents a given node has
def findParents(current_node, startp):
    cost = 0
    while current_node.getCords() != startp:
        current_node = current_node.getParent()
        cost = cost + 1
    return cost


# This is for Problem 2 DFS
def DFS(start, goal):
    # Begin by adding the starting location
    fringe_stack = []
    visited = []
    start_dfs = Node(start[0], start[1], Node)
    fringe_stack.append(start_dfs)
    while fringe_stack:
        # Pop off from the stack and add it to the visited list
        current_node = fringe_stack.pop()
        visited.append(current_node)
        current_position = current_node.getCords()
        current_x = current_position[0]
        current_y = current_position[1]
        # If current position is the goal position return the list
        if current_position == goal:
            return visited
        # check if each move direction is a valid move, do for next 3 possible positions
        if canMove(current_x, current_y - 1):
            next_node = Node(current_x, current_y - 1, current_node)
            fringe_stack.append(next_node)
        if canMove(current_x - 1, current_y):
            next_node = Node(current_x - 1, current_y, current_node)
            fringe_stack.append(next_node)
        if canMove(current_x, current_y + 1):
            next_node = Node(current_x, current_y + 1, current_node)
            fringe_stack.append(next_node)
        if canMove(current_x + 1, current_y):
            next_node = Node(current_x + 1, current_y, current_node)
            fringe_stack.append(next_node)
    # if the while loop ends with no return then the stack is empty and the goal is unreachable
    return []


# This is for Problem 3 BFS
def BFS(start, goal):
    # Begin by adding the starting location
    fringe_queue = []
    visited = []
    start_dfs = Node(start[0], start[1], Node)
    fringe_queue.append(start_dfs)
    while fringe_queue:
        # Pop off from the queue and add it to the visited list
        current_node = fringe_queue.pop(0)
        visited.append(current_node)
        current_position = current_node.getCords()
        current_x = current_position[0]
        current_y = current_position[1]
        # If current position is the goal position return the list
        if current_position == goal:
            return visited
        # check if each move direction is a valid move, do for next 3 possible positions
        if canMove(current_x, current_y - 1):
            next_node = Node(current_x, current_y - 1, current_node)
            fringe_queue.append(next_node)
        if canMove(current_x - 1, current_y):
            next_node = Node(current_x - 1, current_y, current_node)
            fringe_queue.append(next_node)
        if canMove(current_x, current_y + 1):
            next_node = Node(current_x, current_y + 1, current_node)
            fringe_queue.append(next_node)
        if canMove(current_x + 1, current_y):
            next_node = Node(current_x + 1, current_y, current_node)
            fringe_queue.append(next_node)
    # if the while loop ends with no return then the stack is empty and the goal is unreachable
    return visited


# This is for problem 3 AStar
def AStar(start, goal):
    # Begin by adding the start to a heapq
    fringe_heap = []
    visited = []
    start_a = Node(start[0], start[1], Node)
    distance = ((((start[0] - goal[0]) ** 2) + ((start[1] - goal[1]) ** 2)) ** .5)
    start_a.giveH(distance)
    heapq.heappush(fringe_heap, start_a)
    while fringe_heap:
        # popping off the first position in the heapq will give the smallest node to expand
        current_node = heapq.heappop(fringe_heap)
        visited.append(current_node)
        current_position = current_node.getCords()

        current_x = current_position[0]
        current_y = current_position[1]
        cost = current_node.getCost() + 1

        # If current position is the goal position return the list
        if current_position == goal:
            return visited
        # check if each move direction is a valid move, do for next 3 possible positions
        # if each move is possible find the cost and current distance to get h and push to heapq
        if canMove(current_x, current_y - 1):

            new_distance = ((((current_x - goal[0]) ** 2) + (((current_y - 1) - goal[1]) ** 2)) ** .5)
            next_node = Node(current_x, current_y - 1, current_node)
            next_node.addParent(cost)
            h = cost + new_distance
            next_node.giveH(h)
            heapq.heappush(fringe_heap, next_node)

        if canMove(current_x - 1, current_y):
            new_distance = (((((current_x - 1) - goal[0]) ** 2) + ((current_y - goal[1]) ** 2)) ** .5)
            next_node = Node(current_x - 1, current_y, current_node)
            next_node.addParent(cost)
            h = cost + new_distance
            next_node.giveH(h)
            heapq.heappush(fringe_heap, next_node)

        if canMove(current_x, current_y + 1):
            new_distance = ((((current_x - goal[0]) ** 2) + (((current_y + 1) - goal[1]) ** 2)) ** .5)
            next_node = Node(current_x, current_y + 1, current_node)
            next_node.addParent(cost)
            h = cost + new_distance
            next_node.giveH(h)
            heapq.heappush(fringe_heap, next_node)

        if canMove(current_x + 1, current_y):
            new_distance = (((((current_x + 1) - goal[0]) ** 2) + ((current_y - goal[1]) ** 2)) ** .5)
            next_node = Node(current_x + 1, current_y, current_node)
            next_node.addParent(cost)
            h = cost + new_distance
            next_node.giveH(h)
            heapq.heappush(fringe_heap, next_node)
    # if the while loop ends with no return then the stack is empty and the goal is unreachable
    return []


# advance the fire for each time step using probability q
def advance_fire_one_stp(current_maze, q):
    maze_fire = [x[:] for x in maze_copy]
    # maze_fire = current_maze.copy()
    # q = .1
    for row in range(size):
        for col in range(size):
            if current_maze[row][col] == 'w' or maze_copy[row][col] == 'c':
                fire_count = 0
                if row + 1 < size and maze_copy[row + 1][col] == 'f':
                    fire_count = fire_count + 1
                if row - 1 >= 0 and maze_copy[row - 1][col] == 'f':
                    fire_count = fire_count + 1
                if col + 1 < size and maze_copy[row][col + 1] == 'f':
                    fire_count = fire_count + 1
                if col - 1 >= 0 and maze_copy[row][col - 1] == 'f':
                    fire_count = fire_count + 1
                prob = 1 - ((1 - q) ** fire_count)
                prob = prob * 100
                r = randint(1, 100)
                if r <= prob:
                    maze_fire[row][col] = 'f'
    for x in range(size):
        for y in range(size):
            if maze_fire[x][y] == 'f':
                maze_copy[x][y] = 'f'
    return maze_fire


# strategy 1 implementation
def move_robot_s1(final_path, maze3, q):
    paths1 = final_path.copy()
    paths1.pop(0)
    # for each spot in the path advance fire and return maze until either robot dies or robot gets out
    print(paths1)
    for z in range(len(paths1)):
        robot = paths1[z]
        advance_fire_one_stp(maze3, q)
        current_location = paths1[z]
        if maze3[current_location[0]][current_location[1]] == 'f':
            holder = display(maze3)
            holder.mainloop()
            print('You failed')
            return False
        maze3[robot[0]][robot[1]] = 'g'

    return True


# strategy 2 implementation
def move_robot_s2(final_path, maze3, q):
    # going through the first path, re-calculate the path at each step
    while final_path:
        final_path.append(goal_position)
        final_path.pop(0)
        robot = final_path.pop(0)
        if robot == goal_position:
            return True
        advance_fire_one_stp(maze3, q)
        # reset maze back to default so old visited nodes don't interfere with new path
        for x in range(size):
            for y in range(size):
                if maze3[x][y] == 'c':
                    maze3[x][y] = 'w'
        # get the new path
        new_path1 = AStar(robot, goal_position)
        if new_path1:
            up2 = new_path1[len(new_path1) - 1].getParent()
            full_path2 = [up2.getCords()]
            while up2.getCords() != robot:
                up2 = up2.getParent()
                full_path2.append(up2.getCords())
            full_path2 = full_path2[::-1]
            final_path = full_path2
        else:
            print('cant')
            return False
        # holder = display(maze_copy)
        print(final_path)
        # holder.mainloop()
        current_location = robot
        # if the current location the robot is at burns while the robot is there, maze failed
        if maze3[current_location[0]][current_location[1]] == 'f':
            print('death')
            return False
    return True


# creates a secondary maze with integers to show how close a given square is to the initial fire
def danger(maze_in, f_x, f_y, q):
    danger_maze = [[0 for _ in range(size)] for _ in range(size)]
    # go throw the maze and find the current position of all the fire
    # look ahead one step and assign it q, if q is already there add onto it to signal the higher prob of
    # catching fire
    for x in range(size):
        for y in range(size):
            if maze_copy[x][y] == 'P':
                danger_maze[x][y] = 5
            elif maze_copy[x][y] == 'f':
                danger_maze[x][y] = 4
                if x + 1 < size:
                    c = danger_maze[x + 1][y]
                    danger_maze[x+1][y] = c + q
                if x - 1 >= 0:
                    c = danger_maze[x - 1][y]
                    danger_maze[x-1][y] = c + q
                if y + 1 < size:
                    c = danger_maze[x][y + 1]
                    danger_maze[x][y+1] = c + q
                if y - 1 >= 0:
                    c = danger_maze[x][y - 1]
                    danger_maze[x][y - 1] = c + q
    # print(danger_maze)
    return danger_maze


# strategy 3 implementation
def move_robot_s3(maze3, f_x, f_y, start, goal, q):
    danger_maze = danger(maze3, f_x, f_y, q)
    # Begin by adding the starting location
    fringe_stack = []
    visited = []
    start_s3 = Node(start[0], start[1], Node)
    fringe_stack.append(start_s3)
    while fringe_stack:
        # Look for the smallest probability a square can catch fire
        danger_cords = fringe_stack[0].getCords()
        danger_probability = danger_maze[danger_cords[0]][danger_cords[1]]
        shortest = 0
        # find the lowest integer in the danger array to simulate going around where the fire will be
        for k in range(len(fringe_stack)):
            danger_cords = fringe_stack[k].getCords()
            new_danger_probability = danger_maze[danger_cords[0]][danger_cords[1]]
            if new_danger_probability < danger_probability:
                danger_probability = new_danger_probability
                shortest = k
        current_node = fringe_stack.pop(shortest)
        visited.append(current_node)
        current_position = current_node.getCords()
        current_x = current_position[0]
        current_y = current_position[1]
        # If current position is the goal position return the list
        if current_position == goal:
            return visited
        # check if each move direction is a valid move, do for next 3 possible positions
        if canMove(current_x, current_y - 1):
            next_node = Node(current_x, current_y - 1, current_node)
            fringe_stack.append(next_node)
        if canMove(current_x - 1, current_y):
            next_node = Node(current_x - 1, current_y, current_node)
            fringe_stack.append(next_node)
        if canMove(current_x, current_y + 1):
            next_node = Node(current_x, current_y + 1, current_node)
            fringe_stack.append(next_node)
        if canMove(current_x + 1, current_y):
            next_node = Node(current_x + 1, current_y, current_node)
            fringe_stack.append(next_node)
    # if the while loop ends with no return then the stack is empty and the goal is unreachable
    return []


# strategy 2 implementation
def new_s3(final_path, maze3, q, fx, fy, start, goal):
    # going through the first path, re-calculate the path at each step
    while final_path:
        final_path.append(goal_position)
        final_path.pop(0)
        robot = final_path.pop(0)
        if robot == goal_position:
            return True
        advance_fire_one_stp(maze3, q)
        # reset maze back to default so old visited nodes don't interfere with new path
        for x in range(size):
            for y in range(size):
                if maze3[x][y] == 'c':
                    maze3[x][y] = 'w'
        # get the new path
        new_path1 = move_robot_s3(maze_copy, fx, fy, robot, goal, q)
        # print(new_path1)
        if new_path1:
            up2 = new_path1[len(new_path1) - 1].getParent()
            full_path2 = [up2.getCords()]
            while up2.getCords() != robot:
                up2 = up2.getParent()
                full_path2.append(up2.getCords())
            full_path2 = full_path2[::-1]
            final_path = full_path2
        else:
            print('cant')
            return False
        # maze3[robot[0]][robot[1]] = 'g'
        # holder = display(maze_copy)
        # print(final_path)
        # holder.mainloop()
        current_location = robot
        # if the current location the robot is at burns while the robot is there, maze failed
        if maze3[current_location[0]][current_location[1]] == 'f':
            print('death')
            return False
    return True


# display the maze as a GUI
def display(display_maze):
    window1 = Tk()
    window1.title('Fire Maze')
    canvas_side1 = size * cell_size
    ffs1 = Canvas(window1, width=canvas_side1, height=canvas_side1, bg='grey')
    ffs1.pack()
    create(ffs1, display_maze)
    return window1


# create the maze with given p and dimensions
createMaze()
# create a copy of the maze for changing
maze_copy = [x[:] for x in maze]
# start and goal positions of the maze
start_position = [0, 0]
goal_position = [size - 1, size - 1]

runnable = True

while runnable:
    # for each run create a new copy of the original maze
    maze_copy = [x[:] for x in maze]
    print('Would you like fire maze or regular maze (F/R)')
    type_maze = input()
    # all options are for a fire maze
    # F not completely implemented, more for testing fire strategies on a single maze
    if type_maze == "F":
        fire_x = randint(1, size - 1)
        fire_y = randint(1, size - 1)
        fire_position = [fire_x, fire_y]
        # path = DFS(start_position, fire_position)
        # finds a position in the maze that is not a wall, goal or start position
        while maze_copy[fire_x][fire_y] != 'w':
            fire_position = [fire_x, fire_y]
            # path = DFS(start_position, fire_position)
            fire_x = randint(1, size - 1)
            fire_y = randint(1, size - 1)
        # adds the fire location to both mazes


        # print(maze_copy[fire_x][fire_y])
        # window2 = display(maze_copy)
        # window2.mainloop()
        # find if a path can be found to reach the goal position
        # if not scrap the maze
        path = AStar(start_position, goal_position)
        maze_copy = [x[:] for x in maze]
        print(fire_x)
        print(fire_y)
        maze_copy[fire_x][fire_y] = 'f'
        w = display(maze_copy)
        w.mainloop()
        # if a path exists to the goal continue with strategy
        if path:
            print('start')
            up = path[len(path) - 1].getParent()
            full_path = [up.getCords()]
            while up.getCords() != start_position:
                up = up.getParent()
                full_path.append(up.getCords())
            full_path = full_path[::-1]
            print(full_path)
            # use the path for mainly strategy 1 and 2
            if move_robot_s2(full_path, maze_copy, .1):
                print('success')
        window2 = display(maze_copy)
        window2.mainloop()
    elif type_maze == "R":
        # all the options for the regular maze
        print('Would you like BFS, DFS or AStar')
        window = display(maze_copy)
        strategy = input()
        window.destroy()
        # executes the BFS strategy on the given maze
        if strategy == "BFS":
            path = BFS(start_position, goal_position)
            if path:
                # adds the letter 'x' to represent the visited nodes of the maze
                for i in range(len(path) - 1):
                    holder = path[i].getCords()
                    maze_copy[holder[0]][holder[1]] = 'x'

                up = path[len(path) - 1].getParent()
                full_path = [up.getCords()]
                while up.getCords() != start_position:
                    up = up.getParent()
                    full_path.append(up.getCords())

                full_path = full_path[::-1]
                # adds the letter 'g' to represent the final path of the maze given by BFS
                for i in range(len(full_path)):
                    holder = full_path[i]
                    maze_copy[holder[0]][holder[1]] = 'g'
                maze_copy[0][0] = 's'
                window2 = display(maze_copy)
                window2.mainloop()
                print('this maze is possible')
                print(len(full_path))
            else:
                print('cant make it')
        # executes the DFS strategy on the given maze
        if strategy == "DFS":
            path = DFS(start_position, goal_position)
            if path:
                # adds the letter 'x' to represent the visited nodes of the maze
                for i in range(len(path) - 1):
                    holder = path[i].getCords()
                    maze_copy[holder[0]][holder[1]] = 'x'

                up = path[len(path) - 1].getParent()
                full_path = [up.getCords()]
                while up.getCords() != start_position:
                    up = up.getParent()
                    full_path.append(up.getCords())

                full_path = full_path[::-1]
                # adds the letter 'g' to represent the final path of the maze given by BFS
                for i in range(len(full_path)):
                    holder = full_path[i]
                    maze_copy[holder[0]][holder[1]] = 'g'
                maze_copy[0][0] = 's'
                window2 = display(maze_copy)
                window2.mainloop()
                print('this maze is possible')
                print(len(full_path))
            else:
                print('cant make it')
        # executes the A* strategy on the given maze
        if strategy == "AStar":
            path = AStar(start_position, goal_position)
            if path:
                # adds the letter 'x' to represent the visited nodes of the maze
                for i in range(len(path) - 1):
                    holder = path[i].getCords()
                    maze_copy[holder[0]][holder[1]] = 'x'

                up = path[len(path) - 1].getParent()
                full_path = [up.getCords()]
                while up.getCords() != start_position:
                    up = up.getParent()
                    full_path.append(up.getCords())

                full_path = full_path[::-1]
                # adds the letter 'g' to represent the final path of the maze given by BFS
                for i in range(len(full_path)):
                    holder = full_path[i]
                    maze_copy[holder[0]][holder[1]] = 'g'
                maze_copy[0][0] = 's'
                window2 = display(maze_copy)
                window2.mainloop()
                print('this maze is possible')
                print(len(full_path))
            else:
                print('cant make it')
    elif type_maze == '2':
        # gets the results for the problem 2 question
        coord_size = [size]
        # all the p values that are to be tested with the initial size given at run time
        coord_p = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
        success_rate = []
        for s in range(len(coord_p)):
            current_percent = 0
            p = coord_p[s]
            # for every probability try 100 different mazes
            for i in range(100):
                maze = [['w' for _ in range(size)] for _ in range(size)]
                createMaze()
                maze_copy = [x[:] for x in maze]
                cp = coord_p[s]
                path = DFS(start_position, goal_position)
                # if a path is found current_percent ++1, after gets added to an array at the end to be plotted
                if path:
                    current_percent = current_percent + 1
            success_rate.append(current_percent)
        print(success_rate)
        plt.plot(coord_p, success_rate)
        plt.show()
    elif type_maze == '3':
        # gets the results for problem 3 questions
        coord_size = [size]
        # all the p values that are to be tested with the initial size given at run time
        coord_p = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
        average_explored_BFS = []
        average_explored_AStar = []
        for s in range(len(coord_p)):
            current_numberBFS = 0
            current_numberA = 0
            p = coord_p[s]
            print(p)
            # for every probability try 100 different mazes
            for i in range(20):
                print(i)
                maze = [['w' for _ in range(size)] for _ in range(size)]
                createMaze()
                maze_copy = [x[:] for x in maze]
                cp = coord_p[s]
                path = BFS(start_position, goal_position)
                maze_copy = [x[:] for x in maze]
                path2 = AStar(start_position, goal_position)
                # if a path is found current_explored +1, after gets added to an array at the end to be plotted
                # to get nodes if there is no final path, the last return statement in A* and BFS
                # will need to be changed to return visited instead of []
                current_numberBFS = current_numberBFS + len(path)
                current_numberA = current_numberA + len(path2)

            average_explored_BFS.append(current_numberBFS / 20)
            average_explored_AStar.append(current_numberA / 20)
        plt.plot(coord_p, average_explored_BFS, color='red', label='BFS')
        plt.plot(coord_p, average_explored_AStar, color='blue', label='A*')
        plt.xlabel('Obstacle Probability')
        plt.ylabel('Average explored Nodes')
        plt.title('Explored Nodes by Obstacle p')
        plt.legend()
        plt.show()
    elif type_maze == '4':
        # gets the results for the problem 4 question
        total_seconds = 0
        # will take current time and time after run to see how long obtaining each path took
        while total_seconds < 60:
            maze = [['w' for _ in range(size)] for _ in range(size)]
            createMaze()
            maze_copy = [x[:] for x in maze]
            today = datetime.now()
            # change search here
            # path = DFS(start_position, goal_position)
            # path = BFS(start_position, goal_position)
            print(size)
            path = AStar(start_position, goal_position)
            today2 = datetime.now()
            difference = today2 - today
            total_seconds = difference.total_seconds()
            print(total_seconds)
            if path:
                size = size + 100
        print(size)
    elif type_maze == '5':
        # will test each fire strategy and get success rate
        coord_q = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
        success_rate = []
        for k in range(len(coord_q)):
            success_amount = 0
            print(k)
            # will run 20 unique mazes
            for s in range(20):
                maze = [['w' for _ in range(size)] for _ in range(size)]
                createMaze()
                maze_copy = [x[:] for x in maze]
                new_path = AStar(start_position, goal_position)
                # will create a maze until there is a path to the goal
                while not new_path:
                    maze = [['w' for _ in range(size)] for _ in range(size)]
                    createMaze()
                    maze_copy = [x[:] for x in maze]
                    new_path = AStar(start_position, goal_position)
                # print(full_path)
                # will run each unique maze 20 times with new initial fire
                for i in range(10):
                    maze_copy = [x[:] for x in maze]
                    fire_x = randint(1, size - 1)
                    fire_y = randint(1, size - 1)
                    fire_position = [fire_x, fire_y]
                    path = DFS(start_position, fire_position)
                    # if there is no path to the fire, try new spots until there is
                    while not path:
                        maze_copy = [x[:] for x in maze]
                        fire_x = randint(1, size - 1)
                        fire_y = randint(1, size - 1)
                        fire_position = [fire_x, fire_y]
                        path = AStar(start_position, fire_position)
                    # reset maze to default with initial fire position as to not mess with search
                    maze_copy = [x[:] for x in maze]
                    maze_copy[fire_x][fire_y] = 'f'
                    # gets the first path to goal, for strat1/2 this would change to bfs or A*
                    # here is for strat3 with our own search algo
                    new_path2 = move_robot_s3(maze_copy, fire_x, fire_y, start_position, goal_position, coord_q[k])
                    # if path exists with fire location
                    if new_path2:
                        up = new_path2[len(new_path2) - 1].getParent()
                        full_path = [up.getCords()]
                        while up.getCords() != start_position:
                            up = up.getParent()
                            full_path.append(up.getCords())

                        full_path = full_path[::-1]
                        # start given strategy, send path and all necessary info to run each strat
                        # change to strat1 or 2 here
                        if new_s3(full_path, maze_copy, coord_q[k], fire_x, fire_y, start_position, goal_position):
                            # print(coord_q[k], 'success')
                            success_amount = success_amount + 1
                            print(success_amount)
                        else:
                            print('fail')
            # add success rate to array
            success_rate.append(success_amount/2)
            print(success_rate)
        print(success_rate)
        plt.plot(coord_q, success_rate, color='red', label='Strategy2')
        plt.xlabel('Fire Flammability q')
        plt.ylabel('Success Rate(%)')
        plt.title('q by Success')
        plt.legend()
        plt.show()
    elif type_maze == '6':
        # this is mainly for plotting all values gotten from '5'
        coord_q = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
        s1_r = [71.5, 53.5, 32.5, 18.0, 5.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        s2_r = [92, 68, 46.5, 17.5, 7.0, 2.0, 0.0, 1.0, 0.0, 0.0]
        s3_r = [95.5, 73, 56, 26, 13.5, 2.5, 1, 1.5, 0, 0]
        plt.plot(coord_q, s1_r, color='blue', label='Strategy1')
        plt.plot(coord_q, s2_r, color='red', label='Strategy2')
        plt.plot(coord_q, s3_r, color='green', label='Strategy3')
        plt.xlabel('Fire Flammability q')
        plt.ylabel('Success Rate(%)')
        plt.title('q by Success')
        plt.legend()
        plt.show()
    print('would you like to continue Y or N')
    con = input()
    if con == 'N':
        runnable = False
