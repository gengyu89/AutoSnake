# automatic snake game created by: Yu Geng
# 2020-07-31

import shutil
import tkinter as tk
from Piegame.automate import *


if __name__ == '__main__':
    
    # obtain system resolution
    root = tk.Tk()
    system_width  = root.winfo_screenwidth()
    system_height = root.winfo_screenheight()
    
    # clean up previous output
    if os.path.isdir(CAPDIR):
        shutil.rmtree(CAPDIR)
    
    # clean up the terminal
    os.system("clear")
    mainLoop(system_width, system_height)
    
    # to capture a video
    # please uncomment showMoves(N_moves) in runSnakeAI()

