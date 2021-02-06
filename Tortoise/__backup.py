# discarded codes go here
# 2020-07-30

def wander_new():
    """Uses a virtual snake to predict the outcome and
    decides the next move randomly."""
    
    print("Wandering...")
    
    direction = currentDir()
    if virtualGameOver(direction):
        pass
    else:
        print("Maintain current direction.")
        return
    
    options = ['up', 'down', 'left', 'right']
    random.shuffle(options)
    
    # exclude options that are absolutely dead
    feasible = []
    for option in options:
        if virtualGameOver(option) == "dead":
            pass
        else:
            feasible.append(option)
    
    if feasible == []:
        print("All four directions dead!")
        print("")
        return False  # skip the rest of the function
    
    # exclude options that could be dangerous
    next_move = None
    for option in feasible:
        if virtualGameOver(option) == "dangerous":
            print("Replanning route...")
            continue
        else:
            next_move = option
            break
    
    # if too strict, release the second condition
    if next_move is None:
        next_move = feasible[0]
    
    # give the snake an order
    if next_move == 'up':
        moveUp()
    elif next_move == 'down':
        moveDown()
    elif next_move == 'left':
        moveLeft()
    elif next_move == 'right':
        moveRight()

