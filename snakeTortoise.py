# automatic snake game created by: Yu Geng
# 2020-07-28

import os
from Tortoise.automate import *

if __name__ == '__main__':
    
    os.system("clear")
    
    setup(W_screen, H_screen, set_X, set_Y)
    title("")
    hideturtle()
    tracer(False)
    listen()
    
    # key controls
    # onkey(moveRight, 'Right')
    # onkey(moveLeft,  'Left')
    # onkey(moveUp,    'Up')
    # onkey(moveDown,  'Down')
    
    moveSnakeAuto()  # moveSnake() calls itself iteratively
    done()

