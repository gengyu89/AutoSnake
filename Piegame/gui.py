# parameters for rendering pygame objects created by: Yu Geng
# 2020-08-01

import sys, random, pygame

from pygame.locals import *
from Piegame.base import square, vector

# each subroutine initializes BESTMOVE to None
# if it is not able to update BESTMOVE,
# you may check it with BESTMOVE is None

BESTMOVE = None
PYGAMEWIDTH  = 200  # default: 800
PYGAMEHEIGHT = 160  # default: 500
FPS = 17  # determines the speed of the game
CELLSIZE = 20

# other usable sizes:
#   
#   360 - so that you have exactly
#       18 by 18 grids for testing
#   400 - for demonstration
#   240 - for doing research
#   160 - for making gif
#   

# remove hard-coded RGB values
color_FOOD = (255, 0, 0)
color_HEAD = (0, 127, 255)
color_GRIDS = (40, 40, 40)  # borrowed from Al Sweigart
color_BORDER = (128, 128, 128)  # brighter than the grid lines
color_SCORE = (40, 40, 40, 128)  # opacity does not work for pygame.draw.rect()
color_BONES = (255, 255, 255)

# parameters for rendering
SIZESQ = 0.5*CELLSIZE  # size of each segment to be rendered
OFFSET = 0.5*(CELLSIZE-SIZESQ)  # offset from the corner
PAUSETIME = int(15e3)  # time for displaying the final frame [ms]

# be aware that if the render unit is smaller than
# half of the cell size, you will need to make
# more than one conenctor block in showSnake()

