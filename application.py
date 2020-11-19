import keyboard
import graphics as G
import sub_graphics
from classes import *
import time
import random

def main():
    windowSize = 500
    boardSize = 15
    print("Building Window...")
    mainWin = G.GraphWin("Snake", windowSize, windowSize)
    mainWin.setBackground(color_rgb(35,35,35))
    print("Done.")
    print("Building Board and Snake...")
    curBoard = Board(boardSize)
    curSnake = makeRandomSpawn(mainWin,curBoard)
    print("Done.")

    print("Starting Loop...")
    curBoard.spawnFood(mainWin)
    clk = InternalClock(0.2,0,50)
    aliveSnake = True
    while aliveSnake:
        curSnake.getKeyChange(clk.beat())
        aliveSnake = curBoard.step(mainWin,curSnake)




    mainWin.getMouse() # Pause to view result
    mainWin.close()    # Close window when done

def makeRandomSpawn(win,brd):
    p1 = (random.randint(4,brd.size-4),random.randint(4,brd.size-4))
    options = [(0,-1) , (1,0) , (0,1) , (-1,0)]
    dir = options.pop(random.randint(0,3))
    choice = random.choice(options)
    p2 = (p1[0]+choice[0],p1[1]+choice[1])
    p3 = (p2[0]+choice[0],p2[1]+choice[1])
    snk = Snake([p3,p2,p1],dir)
    brd.drawBox(win,p1)
    brd.drawBox(win,p2)
    brd.drawBox(win,p3)
    return snk

main()

"""
curB = Board(50)
for a in range(51):
    time.sleep(0.05)
    curB.drawBox(mainWin,(a,a),food=True)
    if a>2:
        curB.deleteBox((a-3,a-3))
"""