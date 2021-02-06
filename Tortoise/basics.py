# a module that implements keyboard operations and objects
# 2020-07-28

from turtle import *
from random import randrange
from Tortoise.base import square, vector

# parameters for game objects
Margin = 10  # used for detecting boundaries
sizeHead =  8  # width of the snake body
stepSize = 10  # used for updating the aim vector

# create game objects
food  =  vector(-stepSize, 0)
snake = [vector(stepSize, 0)]
aim   =  vector(0, -stepSize)

# To test findLongestPath(), snake must have
#   at least two segments:
snake = [vector(0, 0), vector(stepSize, 0)]

# Use this to create a much longer snake:
# snake = [vector(x, 0) for x in range(0, 50, stepSize)]

# parameters for the game window
W_screen = 110  # default: 420
H_screen = 110  # default: 420
W_half = W_screen//2  # half window size
H_half = H_screen//2
set_X, set_Y = 370, 0  # old: 540, 600
FPS = 60
Interv = int(1e3/FPS)  # by default 100 ms

# other usable sizes:
#   420 - packt default value
#   410 - the smallest to not have scrolling bars
#   230 - this will give you the size
#       of the widely-known example from russia
#   110 - so that you have exactly
#       8 by 8 grids in the graph for testing
#   70 - the smallest you can use
#       to accommodate a snake with only two segments

# other usable speed:
#   100 - packt default value
#   10 - this seems to be the speed of the gif

def change(x, y):
    "Update the aim vector."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    x_lower = - W_half + Margin
    x_upper =   W_half - 2 * Margin
    y_lower = - H_half + Margin
    y_upper =   H_half - 2 * Margin
    return x_lower < head.x < x_upper and y_lower < head.y < y_upper

def getGrids():
    """Discretize the game screen into grids that can be
    reached via only valid moves made by the snake."""
    
    x_lower = round(- W_half + Margin + stepSize//2, -1)
    x_upper = W_half - 2 * Margin
    y_lower = round(- H_half + Margin + stepSize//2, -1)
    y_upper = H_half - 2 * Margin
    
    x_range = range(x_lower, x_upper, stepSize)
    y_range = range(y_lower, y_upper, stepSize)
    
    return x_range, y_range

# calculate the number of grids
# and store it globally
x_range, y_range = getGrids()
N_grids = len(x_range) * len(y_range)

def moveSnake():
    "Move snake forward one segment."
    head = snake[-1].copy()
    head.move(aim)
    
    if not inside(head) or head in snake:
        square(head.x, head.y, sizeHead, 'red')
        N_scores = len(snake)
        update()
        print('Score: %d' % N_scores)
        print('Percentage of coverage: %f' % N_scores/N_grids*1e2)
        return
    
    snake.append(head)  # add the new head to the snake body
    
    if head == food:
        # print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)  # remove the tail element
    
    clear()
    
    # re-render all objects
    drawSnake()
    square(food.x, food.y, sizeHead, 'green')
    update()
    ontimer(moveSnake, Interv)

def drawSnake():
    """Subroutine for rendering the snake object."""
    
    # draw connectors between segments
    for i, current in enumerate(snake):
        if i != 0:
            previous = snake[i-1]
            x = 0.5 * (previous.x + current.x)
            y = 0.5 * (previous.y + current.y)
            square(x, y, sizeHead, 'black')
    
    # draw segments
    for body in snake:
        square(body.x, body.y, sizeHead, 'black')

