# subroutines for automating the snake (virtual snake approach)
# 2020-07-31

import os, math

from Piegame.gui import *
from pygame import gfxdraw
from itertools import product

# check validity before continuing
assert PYGAMEWIDTH  % CELLSIZE == 0, "Width is not divisible!"
assert PYGAMEHEIGHT % CELLSIZE == 0, "Height is not divisible!"
X_GRID = range(0, PYGAMEWIDTH, CELLSIZE)
Y_GRID = range(0, PYGAMEHEIGHT, CELLSIZE)

# parameters for rendering canvas
MATRIX_W = PYGAMEWIDTH//CELLSIZE
MATRIX_H = PYGAMEHEIGHT//CELLSIZE
MATRIX_SIZE = MATRIX_W * MATRIX_H
BGCOLOR = (0, 0, 0)

# parameters for refreshing the canvas
CAPDIR = './capture/'
FOODNUM = 0
CKBBOARD = (MATRIX_W + 1) * (MATRIX_H + 1)
MAXLENGTH = 2 * CKBBOARD  # used for finding shortest paths
MOVEDIR = {'U': -MATRIX_W, 'D': MATRIX_W, \
           'L': -1, 'R': 1,}  # this can be done with enum in C++

# ----- Subroutines for rendering objects -----

def drawGrid():
    """Subroutine for displaying
    the grid setting - Method I."""
    
    # render grid lines
    thickness = math.ceil(0.1*CELLSIZE)
    for X in X_GRID:
        pygame.draw.line(screen, color_BORDER, (X, 0), (X, PYGAMEHEIGHT))
    for Y in Y_GRID:
        pygame.draw.line(screen, color_BORDER, (0, Y), (PYGAMEWIDTH, Y))
    
    # render the borders
    # pygame.draw.line(screen, color_BORDER, \
    #     (0, 0), (0, PYGAMEHEIGHT))  # left
    # pygame.draw.line(screen, color_BORDER, \
    #     (PYGAMEWIDTH-1, 0), (PYGAMEWIDTH-1, PYGAMEHEIGHT))  # right
    # pygame.draw.line(screen, color_BORDER, \
    #     (0, 0), (PYGAMEWIDTH, 0))  # top
    # pygame.draw.line(screen, color_BORDER, \
    #     (0, PYGAMEHEIGHT-1), (PYGAMEWIDTH, PYGAMEHEIGHT-1))  # bottom

def drawCenters():
    """Subroutine for displaying
    the grid setting - Method II."""
    
    radius = int(0.1 * CELLSIZE)
    for X, Y in product(X_GRID, Y_GRID):
        x, y = X + CELLSIZE//2, Y + CELLSIZE//2
        pygame.draw.circle(screen, color_GRIDS, (int(x), int(y)), radius)

def showFood(location):
    """A better subroutine than the original
    showApple() function."""
    
    x = (location.x + 0.5) * CELLSIZE
    y = (location.y + 0.5) * CELLSIZE
    radius = int(0.4 * CELLSIZE)
    
    # pygame.draw.rect(), pygame.draw.ellipse(), and pygame.draw.arc()
    # require a pygame.Rect object, but pygame.draw.circle() does not
    
    # render the circle
    pygame.draw.circle(screen, color_BONES, (int(x), int(y)), radius)

def showSnake(coords):
    """Subroutine for rendering the snake body."""
    
    # render the connector blocks
    for i, this in enumerate(coords):
        if i != 0:
            previous = coords[i-1]
            x = 0.5 * (this.x + previous.x) * CELLSIZE
            y = 0.5 * (this.y + previous.y) * CELLSIZE
            inner_rect = pygame.Rect(x + OFFSET, y + OFFSET, SIZESQ, SIZESQ)
            pygame.draw.rect(screen, color_BONES, inner_rect)
    
    # render the head (inner only)
    x = coords[0].x * CELLSIZE
    y = coords[0].y * CELLSIZE
    # head_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    # pygame.draw.rect(screen, (0, 80, 255), head_rect)
    head_inner_rect = pygame.Rect(x + OFFSET, y + OFFSET, SIZESQ, SIZESQ)
    pygame.draw.rect(screen, color_BONES, head_inner_rect)
    
    # render the body (inner only)
    for coord in coords[1:]:
        x = coord.x * CELLSIZE
        y = coord.y * CELLSIZE
        inner_rect = pygame.Rect(x + OFFSET, y + OFFSET, SIZESQ, SIZESQ)
        pygame.draw.rect(screen, color_BONES, inner_rect)

def showMoves(N_move):
    """Subroutine for displaying
    the current frame number."""
    
    # PingFang.ttc is not a mono font
    # Monaco.dfont is somehow wierd for numbers
    
    # construct a text box
    corner_x, corner_y = PYGAMEWIDTH-120, 10
    title_font = pygame.font.Font('Menlo.ttc', 16)
    title_text = title_font.render('Move: %04d' % N_move, True, color_BONES)
    text_rect = title_text.get_rect()
    text_rect.topleft = (corner_x, corner_y)
    
    # render a rectangle
    text_box_rect = pygame.Rect(corner_x - 5, corner_y, \
        text_rect.width + 10, text_rect.height)
    
    # render the text
    pygame.draw.rect(screen, color_SCORE, text_box_rect)
    screen.blit(title_text, text_rect)
    pygame.display.update()

# ----- Subroutines for controlling workflow -----

def closeGame():
    """Closes the game panel."""
    pygame.quit()
    sys.exit()

def echoCoverage(finalLength):
    """Subroutine for calculating the percentage of
    coverage and showing it in the Terminal."""
    
    cover = 1e2 * finalLength / MATRIX_SIZE
    
    print('Final length: %d' % finalLength)
    print('Coverage [_]: %f\n' % cover)

def mainLoop(sys_width, sys_height):
    """Main subroutine for invoking runSnakeAI()."""
    
    # calculate window position
    global screen, clock
    set_X = sys_width  - PYGAMEWIDTH  - 20
    set_Y = sys_height - PYGAMEHEIGHT - 10
    
    pygame.init()
    screen = pygame.display.set_mode((PYGAMEWIDTH, PYGAMEHEIGHT))
    pygame.display.set_caption("Auto Snake")
    clock = pygame.time.Clock()
    
    # without doing anything,
    # the game will start over
    
    while True:
        os.mkdir('capture')
        finalLength = runSnakeAI()
        echoCoverage(finalLength)
        pygame.time.delay(5000)
        closeGame()

def isFree(idx, snake):
    """Determines whether a cell is available
    for placing a refreshed food."""
    
    location_x = idx % MATRIX_W
    location_y = idx // MATRIX_W
    idx = vector(location_x, location_y)
    
    return (idx not in snake)

def refreshFood(snake_coords):
    """Subroutine for refreshing
    the coordinate of the food."""
    
    safe = False
    while not safe:
        respawn_x = random.randint(0, MATRIX_W-1)
        respawn_y = random.randint(0, MATRIX_H-1)
        respawnPoint = vector(respawn_x, respawn_y)
        if respawnPoint not in snake_coords:
            safe = True
    
    return respawnPoint

def resetCanvas(snake, canvas, food):
    """Subroutine for refreshing the game board."""
    fake_canvas = canvas[:]
    food_idx = food.x + food.y * MATRIX_W
    
    for i in range(MATRIX_SIZE):
        if i == food_idx:
            fake_canvas[i] = FOODNUM
        elif isFree(i, snake):
            fake_canvas[i] = CKBBOARD
        else:
            fake_canvas[i] = MAXLENGTH
    
    return fake_canvas

def getHeadCoords(snake_coords, next_move):
    """Returns the snake's head after each move."""
    
    if next_move == 'U':
        newHead = vector(snake_coords[0].x, \
                         snake_coords[0].y - 1)
    elif next_move == 'D':
        newHead = vector(snake_coords[0].x, \
                         snake_coords[0].y + 1)
    elif next_move == 'L':
        newHead = vector(snake_coords[0].x - 1, \
                         snake_coords[0].y)
    elif next_move == 'R':
        newHead = vector(snake_coords[0].x + 1, \
                         snake_coords[0].y)
    
    return newHead

# ----- Subroutines for automating the snake -----

def runSnakeAI():
    """The main function for invoking
    all subroutines for automation."""
    
    lower_x, upper_x = int(0.25*MATRIX_W), int(0.75*MATRIX_W)
    lower_y, upper_y = int(0.25*MATRIX_H), int(0.75*MATRIX_H)
    canvas = [0] * MATRIX_SIZE
    
    snakeArray = []
    start_y = random.randint(lower_y, upper_y)
    for start_x in range(lower_x, upper_x):
        segment = vector(start_x, start_y)
        snakeArray.append(segment)
    
    N_moves = 0
    respawnPoint = refreshFood(snakeArray)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    closeGame()
        
        screen.fill(BGCOLOR)
        drawGrid()  # if necessary
        showSnake(snakeArray)
        showFood(respawnPoint)
        # showMoves(N_moves)
        
        # doing the computation
        reset_canvas = resetCanvas(snakeArray, canvas, respawnPoint)
        canvas = reset_canvas
        result, refresh_canvas = runAstar(snakeArray, respawnPoint, canvas)
        canvas = refresh_canvas
        
        # decide whether to return to main
        if result:
            BESTMOVE = findSafeMove(snakeArray, canvas, respawnPoint)
            # findSafeMove() calls shortestPath() and chaseTail()
        else:
            BESTMOVE = chaseTail(snakeArray, canvas, respawnPoint)
            # chaseTail() calls longestPath()
        if BESTMOVE is None:
            BESTMOVE = almightyMove(snakeArray, canvas, respawnPoint)
        if BESTMOVE is not None:
            new_head = getHeadCoords(snakeArray, BESTMOVE)
            snakeArray.insert(0, new_head)
            head_idx = snakeArray[0].x \
                + snakeArray[0].y * MATRIX_W
            end_idx = snakeArray[-1].x + snakeArray[-1].y * MATRIX_W
            
            if (snakeArray[0].x == respawnPoint.x) \
            and (snakeArray[0].y == respawnPoint.y):
                canvas[head_idx] = MAXLENGTH
                if len(snakeArray) < MATRIX_SIZE:
                    respawnPoint = refreshFood(snakeArray)
            
            else:
                canvas[head_idx] = MAXLENGTH
                canvas[end_idx] = CKBBOARD
                del snakeArray[-1]
        
        else:
            return len(snakeArray)  # I added len(snakeArray) here
        
        # update and capture
        pygame.display.update()
        pygame.image.save(screen, './capture/move_%04d.tga' % N_moves)
        clock.tick(FPS)
        N_moves += 1
        
def runAstar(snake, food, canvas):
    """Subroutine for running the Snake AI
    and refreshing the game window."""
    
    fake_canvas = canvas[:]
    food_idx = food.x + food.y * MATRIX_W
    queue = []
    queue.append(food_idx)
    inqueue = [0] * MATRIX_SIZE
    found = False
    
    print("Using A* search...")
    
    while len(queue) != 0:
        idx = queue.pop(0)
        if inqueue[idx] == 1:
            continue
        
        inqueue[idx] = 1
        for next_move in ['L', 'R', 'U', 'D']:
            if isFeasible(idx, next_move):
                if (idx + MOVEDIR[next_move]) == \
                (snake[0].x + snake[0].y * MATRIX_W):
                    found = True
                
                if fake_canvas[idx + MOVEDIR[next_move]] < MAXLENGTH:
                    if fake_canvas[idx + MOVEDIR[next_move]] > fake_canvas[idx]+1:
                        fake_canvas[idx + MOVEDIR[next_move]] = fake_canvas[idx]+1
                    if inqueue[idx + MOVEDIR[next_move]] == 0:
                        queue.append(idx + MOVEDIR[next_move])
    
    return (found, fake_canvas)

def isFeasible(idx, next_move):
    """Forward checking following the direction
    specified by next_move."""
    # initialize output
    flag = False
    
    if next_move == 'L':
        if idx % MATRIX_W > 0: flag = True
        else: flag = False
    elif next_move == 'R':
        if idx % MATRIX_W < MATRIX_W - 1: flag = True
        else: flag = False
    elif next_move == 'U':
        if idx > MATRIX_W - 1: flag = True
        else: flag = False
    elif next_move == 'D':
        if idx < MATRIX_SIZE - MATRIX_W: flag = True
        else: flag = False
    
    return flag

# ----- Subroutines for making a decision -----

def findSafeMove(snake, canvas, food):
    """Determines a safe path between the head and the food."""
    # initialize output
    safe_move = None
    
    # forward the virtual snake one step
    real_snake  = snake[:]
    real_canvas = canvas[:]
    v_snake, v_canvas = virtualMove(snake, canvas, food)
    
    # calculate coverage
    # coverage = 1e2 * len(snake)/MATRIX_SIZE
    # print('Coverage: %f' % coverage)
    
    # determine the next move
    if isSuggested(v_snake, v_canvas, food):
        # if coverage < 70.0:
        #     safe_move = shortestPath(real_snake, real_canvas)
        # else:
        #     safe_move = longestPath(real_snake, real_canvas)
        #     safe_move = almightyMove(snake, canvas, food)
        safe_move = shortestPath(real_snake, real_canvas)
    else:
        safe_move = chaseTail(real_snake, real_canvas, food)
    
    return safe_move

def isSuggested(snake, canvas, food):
    """Determines if there is a path from
    the head of the snake to its tail."""
    
    fake_canvas = canvas[:]
    fake_snake = snake[:]
    
    end_idx = fake_snake[-1].x + fake_snake[-1].y * MATRIX_W
    fake_canvas[end_idx] = FOODNUM
    v_food = fake_snake[-1]
    
    food_idx = food.x + food.y * MATRIX_W
    fake_canvas[food_idx] = MAXLENGTH
    
    result, refresh_tcanvas = runAstar(fake_snake, v_food, fake_canvas)
    fake_canvas = refresh_tcanvas
    for next_move in ['L', 'R', 'U', 'D']:
        idx = fake_snake[0].x + fake_snake[0].y * MATRIX_W
        end_idx = fake_snake[-1].x + fake_snake[-1].y * MATRIX_W
        if isFeasible(idx, next_move) and \
        (idx + MOVEDIR[next_move] == end_idx) and (len(fake_snake) > 3):
            result = False
    
    return result

def virtualMove(snake, canvas, food):
    """Forwards the snake one step virtually."""
    
    fake_snake = snake[:]
    fake_canvas = canvas[:]
    reset_tcanvas = resetCanvas(fake_snake, fake_canvas, food)
    fake_canvas = reset_tcanvas
    eaten = False
    
    while not eaten:
        refresh_tcanvas = runAstar(fake_snake, food, fake_canvas)[1]
        fake_canvas = refresh_tcanvas
        next_move = shortestPath(fake_snake, fake_canvas)
        snake_coords = fake_snake[:]
        fake_snake.insert(0, getHeadCoords(snake_coords, next_move))
        
        if fake_snake[0] == food:
            reset_tcanvas = resetCanvas(fake_snake, fake_canvas, food)
            fake_canvas = reset_tcanvas
            food_idx = food.x + food.y * MATRIX_W
            fake_canvas[food_idx] = MAXLENGTH
            eaten = True
        else:
            newHead_idx = fake_snake[0].x + fake_snake[0].y * MATRIX_W
            fake_canvas[newHead_idx] = MAXLENGTH
            end_idx = fake_snake[-1].x + fake_snake[-1].y * MATRIX_W
            fake_canvas[end_idx] = CKBBOARD
            del fake_snake[-1]
    
    return fake_snake, fake_canvas

# ----- Subroutines for path planning -----

def shortestPath(snake, canvas):
    """Selects the shortest path from the
    four neighbors of the snake's head."""
    BESTMOVE = None
    min_distance = MAXLENGTH
    
    for next_move in ['L', 'R', 'U', 'D']:
        idx = snake[0].x + snake[0].y * MATRIX_W
        if isFeasible(idx, next_move) and \
        (canvas[idx + MOVEDIR[next_move]] < min_distance):
            min_distance = canvas[idx + MOVEDIR[next_move]]
            BESTMOVE = next_move
    
    print("target = food")
    print("BESTMOVE:", BESTMOVE)
    print("")
    
    return BESTMOVE

def longestPath(snake, canvas):
    """Find the longest path from the
    four neighbors of the snake's head."""
    
    BESTMOVE = None
    max_distance = -1
    
    # when searching for the longest path,
    # 'U' and 'D' are preferred directions
    
    for next_move in ['U', 'D', 'L', 'R']:
        idx = snake[0].x + snake[0].y * MATRIX_W
        if isFeasible(idx, next_move) and \
        (canvas[idx + MOVEDIR[next_move]] > max_distance) \
        and (canvas[idx + MOVEDIR[next_move]] < CKBBOARD):
            max_distance = canvas[idx + MOVEDIR[next_move]]
            BESTMOVE = next_move
    
    print("target = tail")
    print("BESTMOVE:", BESTMOVE)
    print("")
    
    return BESTMOVE

def chaseTail(snake, canvas, food):
    """Forwards the snake one step towards its the tail."""
    
    fake_snake = snake[:]
    fake_canvas = resetCanvas(fake_snake, canvas, food)
    
    end_idx = fake_snake[-1].x + fake_snake[-1].y * MATRIX_W
    fake_canvas[end_idx] = FOODNUM
    v_food = fake_snake[-1]
    
    food_idx = food.x + food.y * MATRIX_W
    fake_canvas[food_idx] = MAXLENGTH
    
    result, refresh_tcanvas = runAstar(fake_snake, v_food, fake_canvas)
    fake_canvas = refresh_tcanvas
    
    fake_canvas[end_idx] = MAXLENGTH
    path = longestPath(fake_snake, fake_canvas)
    
    return path

def almightyMove(snake, canvas, food):
    """Takes a random step if there is no possibility."""
    # although desgined as part of the algorithm,
    # this subroutine is never invoked in any situation
    BESTMOVE = None
    
    reset_canvas = resetCanvas(snake, canvas, food)
    canvas = reset_canvas
    result, refresh_canvas = runAstar(snake, food, canvas)
    canvas = refresh_canvas
    min_distance = MAXLENGTH
    
    # vertical moves are preferred directions
    for next_move in ['U', 'D', 'L', 'R']:
        idx = snake[0].x + snake[0].y * MATRIX_W
        if isFeasible(idx, next_move) and \
        (canvas[idx + MOVEDIR[next_move]] < min_distance):
            min_distance = canvas[idx + MOVEDIR[next_move]]
            BESTMOVE = next_move
    
    print("Moving randomly...")
    print("BESTMOVE:", BESTMOVE)
    print("")
    
    return BESTMOVE

