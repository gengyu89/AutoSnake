# subroutines for automating the snake (hamiltonian cycles)
# 2020-07-28

import random, collections

from copy import deepcopy
from Tortoise.basics import *
from itertools import product

# define these as anonymous functions
moveRight = lambda: change( stepSize, 0)
moveLeft  = lambda: change(-stepSize, 0)
moveUp    = lambda: change(0,  stepSize)
moveDown  = lambda: change(0, -stepSize)

# constants for planning the next move
ERR = -404
CALLDICT = {'R': "moveRight()", 'L': "moveLeft()", \
            'U': "moveUp()",    'D': "moveDown()"}

def currentDir():
    """Subroutine for telling the current moving direction."""
    
    if aim.y == stepSize:
        return 'U'
    elif aim.y == -stepSize:
        return 'D'
    elif aim.x == stepSize:
        return 'R'
    elif aim.x == -stepSize:
        return 'L'

def isSafe(target, snake):
    """Determines if any part of the body exists in the rectangular area
    specified by [head.x, target.x] and [head.y, target,y]."""
    # target could be either tail or food
    
    head = snake[-1].copy()
    neighbors = getNeighbors(target)  # do not exclude body segments
    
    # rectangular criteria
    x_lower, x_upper = min(head.x, target.x), max(head.x, target.x)
    y_lower, y_upper = min(head.y, target.y), max(head.y, target.y)
    
    # when x_lower == x_upper,
    # using < will make the condition pointless
    
    for body in snake[:-1]:  # do not include head, include tail
        X_inside = (x_lower <= body.x <= x_upper)
        Y_inside = (y_lower <= body.y <= y_upper)
        if X_inside and Y_inside:
            return False
        elif body in neighbors:
            return False
        else:
            continue
    
    return True

def hasDeadEnd(snake):
    """Returns the area that is dangerous if dead end exists,
    False elsewise."""
    
    L = len(snake)
    for i in range(L):
        pass

def nextMove(target, snake):
    """Subroutine that decides the next move
    according to current food/tail and snake status."""
    
    print("Calling nextMove()...")
    
    head = snake[-1].copy()
    direction = currentDir()
    
    print("Current direction:", direction)
    if target.x < head.x and direction != 'R':
        print("Moving left...")
        moveLeft()
    elif target.x > head.x and direction != 'L':
        print("Moving right...")
        moveRight()
    elif target.y < head.y and direction != 'U':
        print("Moving down...")
        moveDown()
    elif target.y > head.y and direction != 'D':
        print("Moving up...")
        moveUp()
    
    print("Aim:", aim)
    print("")

def dangerous(head):
    """Determines if the snake has entered
    an area surrounded by its body."""
    
    # it is important to exclude the head here
    # if you don't, the statement always produces True
    
    body_x = [body.x for body in snake[:-1]]
    body_y = [body.y for body in snake[:-1]]
    
    dang_x = (min(body_x) <= head.x <= max(body_x))
    dang_y = (min(body_y) <= head.y <= max(body_y))
    
    return dang_x and dang_y

def virtualGameOver(next_move):
    """Uses a virtual snake to tell
    if the next move will result in a problem."""
    
    print("Invoking virtual snake...")
    
    # create duplicates
    snakeVirtual = deepcopy(snake)
    aimVirtual = deepcopy(aim)
    
    # update aim
    if next_move == 'U':
        aimVirtual.x, aimVirtual.y = 0,  stepSize
    elif next_move == 'D':
        aimVirtual.x, aimVirtual.y = 0, -stepSize
    elif next_move == 'R':
        aimVirtual.x, aimVirtual.y =  stepSize, 0
    elif next_move == 'L':
        aimVirtual.x, aimVirtual.y = -stepSize, 0
    
    # update the snake
    headVirtual = snakeVirtual[-1].copy()
    headVirtual.move(aimVirtual)
    
    # determine the outcome
    if not inside(headVirtual) or headVirtual in snakeVirtual:
        print("Virtual snake is dead!")
        print("")
        return "dead"
    elif dangerous(headVirtual):
        print("Warning area!")
        print("")
        return "dangerous"
    else:
        return False

def almighty():
    """Determines a move initiatively even if
    the next move does not result in game over."""
    
    print("Using almighty move...")
    
    next_move = ERR
    options = ['U', 'D', 'R', 'L']  # the order really matters
    
    for option in options:
        if virtualGameOver(option) == "dead":
            print("Replanning route...")
            continue
        else:
            next_move = option
            break
    
    # give the snake an order
    if next_move in CALLDICT.keys():
        exec(CALLDICT[next_move])
    else:
        print("All four directions dead!")
        print("")  # do nothing

def wander():
    """Uses a virtual snake to predict the outcome
    and decides the next move randomly."""
    
    print("Wandering...")
    
    direction = currentDir()
    if not virtualGameOver(direction):
        print("Maintain current direction.")
        return None
    
    options = ['U', 'D', 'L', 'R']
    # random.shuffle(options)  # vertical spiral - preferred pattern
    
    next_move = ERR
    for option in options:
        if virtualGameOver(option) == "dead":
            print("Replanning route...")
            continue
        else:
            next_move = option
            break
    
    # give the snake an order
    if next_move in CALLDICT.keys():
        exec(CALLDICT[next_move])
    else:
        print("All four directions dead!")
        print("")  # do nothing

def planNextMove(food, snake):
    """Subroutine for giving the current snake an order."""
    tail = snake[0].copy()
    
    # AI Mode I:
    # if isSafe(food, snake):
    #     print("target = food")
    #     nextMove(food, snake)
    # else:
    #     almighty()
    
    # AI Mode II:
    if isSafe(food, snake):
        print("target = food")
        nextMove(food, snake)
    else:
        print("target = tail")
        path = longestPathDict()
        if path is None:
            almighty()
        else:
            nextMoveVectors(path)

def updateFood():
    """A better subroutine than the Packt code."""
    
    X_range = W_half//10 * 3//4
    Y_range = H_half//10 * 3//4
    food.x = randrange(-X_range, X_range) * 10
    food.y = randrange(-Y_range, Y_range) * 10
    
    while food in snake:
        food.x = randrange(-X_range, X_range) * 10
        food.y = randrange(-Y_range, Y_range) * 10

def moveSnakeAuto():
    "Automatic version of moveSmake()."
    
    # update aim iteratively
    planNextMove(food, snake)
    
    head = snake[-1].copy()
    head.move(aim)
    
    if not inside(head) or head in snake:
        square(head.x, head.y, sizeHead, 'red')
        update()
        return
    
    snake.append(head)  # add the new head to the snake body
    if head == food:
        # print('Snake:', len(snake))
        updateFood()
    else:
        snake.pop(0)  # remove the tail element
    
    # re-render all objects
    clear()
    drawSnake()  # use my new subroutine to render the snake
    square(food.x, food.y, sizeHead, 'green')
    update()
    ontimer(moveSnakeAuto, Interv)

# ----- Surprises start from here -----

class UndirectedGraph(collections.Sequence):
    """A data structure that allows
    bidirectional traversals."""
    def __init__(self, nodes=None):
        if nodes is None:
            nodes = []
        self.__nodes = nodes

    def InsertNode(self, node):
        if node not in self.__nodes:
            self.__nodes.append(node)

    def __str__(self):
        res = 'Nodes:\n'
        for node in self.__nodes:
            res += (str(node) + '\n')
        return res

class Node(object):
    """Data structure for representing
    each cell on the map."""
    def __init__(self, current, neighbors):
        self.__current = current
        self.__neighbors = neighbors
    
    @property
    def current(self):
        return self.__current  # deepcopy() removed
    
    @property
    def neighbors(self):
        return self.__neighbors  # deepcopy() removed
    
    def __eq__(self, other):
        return self.current == other.current
    
    def __repr__(self):
        name    = self.current
        content = self.neighbors
        return '{!r}: {!r}'.format(name, content)
        # return str(self.current) + ': ' + str(self.neighbors) + '\n'

def getNeighbors(V):
    """Given the coordinate of a cell as a vector,
    returns the coordinates of its four neighbors."""
    
    N_1 = vector(V.x - stepSize, V.y)
    N_2 = vector(V.x + stepSize, V.y)
    N_3 = vector(V.x, V.y - stepSize)
    N_4 = vector(V.x, V.y + stepSize)
    
    return N_1, N_2, N_3, N_4

def isValid(node):
    """Determines if a node is inside of the screen
    and not a part of the snake body."""
    
    # the snake's tail must not be excluded
    # otherwise you will never find a path
    
    return inside(node) and node not in snake[1:]

# ----- Brute Force -----

def createGraphList():
    """Convert the empty space into a directed graph."""
    graph = []
    
    # define valid area - note the difference from inside()
    x_lower = round(- W_half + Margin, -1) + stepSize
    x_upper = W_half - 2 * Margin
    y_lower = round(- H_half + Margin, -1) + stepSize
    y_upper = H_half - 2 * Margin
    
    # enumerate available grids
    x_range = range(x_lower, x_upper, stepSize)
    y_range = range(y_lower, y_upper, stepSize)
    
    # traverse through the canvas
    for X, Y in product(x_range, y_range):
        V = vector(X, Y)  # get the key
        if V in snake:
            pass
        else:
            neighbors = [N for N in getNeighbors(V) if isValid(N)]
            graph.append(Node(V, neighbors))
    
    return graph

def Hamiltonian(traversed, rest, target):
    # traversed and rest are lists of Nodes
    # target is an instance of Vector
    # the returned object has the same structure as a graph
    
    last_node = traversed[-1]
    next_nodes = last_node.neighbors
    
    # examine the base case
    if target in next_nodes:
        return traversed
    elif rest == []:
        print("Target not found!")
        return False
    
    # create deep copies
    traversed = deepcopy(traversed)
    rest = deepcopy(rest)
    deadEnd = True  # determine whether it is a dead end
    paths = []
    print("rest:", rest)
    
    for next_node in next_nodes:
        # print("Current next node:", next_node)
        for rst in rest:
            if next_node == rst.current:
                # print("Next node found!")
                deadEnd = False
                traversed.append(rst)
                rest.remove(rst)
                sol = Hamiltonian(traversed, rest, target)
                if sol:
                    paths.append(sol)
                    print('Total paths found: %d' % len(paths))
            else:
                continue
    
    if deadEnd:
        # print("Next node not found!")
        return False
    else:
        return paths

def longestPathList():
    """Calculate the longest path from
    the current snake head to its tail."""
    
    head = snake[-1].copy()
    neighbors = [N for N in getNeighbors(head) if isValid(N)]
    
    # create the head Node, the graph, and the target
    traversed = [Node(head, neighbors)]
    rest = createGraphList()
    target = snake[0].copy()
    
    print("Computing all paths...")
    
    # call Hamiltonian() to calculate all paths
    paths = list(Hamiltonian(traversed, rest, target))
    L_max = max(list(map(len, paths)))
    
    # find the longest
    for path in paths:
        if len(path) == L_max:
            return path
        else:
            continue

def nextMoveNodes(path):
    """Given a path, decides the next move
    from the first two graph nodes."""
    # path - a list of Nodes
    
    if path is not None and len(path) == 1:
        print("Maintain current direction.")
        print("")
        return None  # skip the rest of the function
    
    print("Next move according to Hamiltonian:")
    head, node_1 = path[0].current, path[1].current
    print(head, node_1)
    
    if head.x < node_1.x:
        print('Right\n')
        moveRight()
    elif head.x > node_1.x:
        print('Left\n')
        moveLeft()
    elif head.y < node_1.y:
        print('Up\n')
        moveUp()
    elif head.y > node_1.y:
        print('Down\n')
        moveDown()

# ----- Dynamic Programming -----

def createGraphDict():
    """Convert the empty space into a directed graph."""
    graph = dict()
    
    # enumerate available grids
    x_range, y_range = getGrids()
    
    # traverse through the canvas
    for X, Y in product(x_range, y_range):
        V = vector(X, Y)  # get the key
        if V in snake:
            pass
        else:
            neighbors = [N for N in getNeighbors(V) if isValid(N)]
            graph[V] = neighbors
    
    return graph

def manhattan(node_1, node_2):
    """Cost computation for the case that
    only four directions' moves are permitted."""

    dist_x = abs(node_2.x - node_1.x)
    dist_y = abs(node_2.y - node_1.y)

    return dist_x + dist_y

def astar(graph, start, end, path=[]):
    """findPath() accelerated with heuristic function;
    used as an alternative to findLongestPath()."""
    
    path = path + [start]
    if start == end:
        return path
    
    # enumerate and sort next choices
    # choices = [N for N in graph[start] if N not in path]
    choices = graph[start]
    choices.sort(key=lambda c: manhattan(c, end), reverse=True)
    
    # since each time you call astar(),
    # start is shifted to the next node,
    # there is no need to compute and sort with G
    
    for node in choices:
        if node not in path:
            longestPath = astar(graph, node, end, path)
            if longestPath:
                return longestPath
    
    return None

def findPath(graph, start, end, path=[]):
    """Find a path within a directed graph,
    without caring whether it is the longest or not."""
    
    path = path + [start]
    if start == end:
        return path
    
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath:
                return newpath
    
    return None

def findRandomPath(graph, start, end, path=[]):
    """Find a path within a directed graph,
    without caring whether it is the longest or not."""
    
    path = path + [start]
    if start == end:
        return path
    
    nodes = graph[start]
    random.shuffle(nodes)
    
    for node in nodes:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath:
                return newpath
    
    return None

def findLongestPath(graph, start, end, path=[]):
    """Hamiltonian() optimized with dynamic programming."""
    
    path = path + [start]
    if start == end:
        return path
    
    longestPath = []
    for node in graph[start]:
        if node not in path:
            newpath = findLongestPath(graph, node, end, path)
            if newpath:
                if not longestPath or len(newpath) > len(longestPath):
                    longestPath = newpath
    
    return longestPath

def longestPathDict():
    """A subroutine that calls findLongestPath()."""
    
    # create a graph for the empty space
    graph = createGraphDict()
    
    # create the end node and add it to the graph
    tail = snake[0].copy()
    graph[tail] = []
    
    # create the start node and add it to the graph
    head = snake[-1].copy()
    neighbors = [N for N in getNeighbors(head) if isValid(N)]
    graph[head] = neighbors
    
    # start is a source that has no edge pointing to it
    # end is a sink that has no going out edge
    
    if tail in neighbors:
        graph[head].remove(tail)
    
    print("Planning...")
    path = astar(graph, head, tail)
    # path = findPath(graph, head, tail)
    # path = findRandomPath(graph, head, tail)
    # path = findLongestPath(graph, head, tail)
    
    return path

def nextMoveVectors(path):
    """Given a path, decides the next move
    from the first two graph nodes."""
    
    if path is not None and len(path) == 1:
        print("Maintain current direction.")
        print("")
        return None  # skip the rest of the function
    
    print("Next move according to Hamiltonian:")
    head, node_1 = path[0], path[1]
    print(head, node_1)
    
    if head.x < node_1.x:
        print('Right\n')
        moveRight()
    elif node_1.x < head.x:
        print('Left\n')
        moveLeft()
    elif head.y < node_1.y:
        print('Up\n')
        moveUp()
    elif node_1.y < head.y:
        print('Down\n')
        moveDown()

