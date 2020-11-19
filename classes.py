from graphics import *
import keyboard
import random

def tplSum(tp1,tp2):
    return (tp1[0]+tp2[0],tp1[1]+tp2[1])

def tplSub(tp1,tp2):
    return (tp1[0]-tp2[0],tp1[1]-tp2[1])

def tplNeg(tp):
    return(-1*tp[0],-1*tp[1])

class Snake:
    #dirDic = {1:(0,-1),2:(1,0),3:(0,1),4:(-1,0)}
    stDic = {
        "flecha arriba":   (0,-1),
        "flecha derecha":  (1,0),
        "flecha abajo":    (0,1),
        "flecha izquierda":(-1,0)}

    def __init__(self,positions,direction):
        self.pos = positions #List of positions that the snake will occupy. First = tail, last = head
        self.dir = direction #(0,-1) = Up, (1,0) = Right, (0,1) = Down, (-1,0) = Left
        self.getNeck() #Position where the snake would go backwards. Not allowed.
        self.pSet = set(positions)

    def getNeck(self):
        self.neck = tplSub(self.pos[-2],self.pos[-1])

    def step(self,board):
        newPos = tplSum(self.pos[-1],self.dir) #New pos that will be occupied based on the direction of the snake
        if (newPos != board.foodPos):
            a = self.pos.pop(0)
            self.pSet.remove(a)
        else: #This happens when the snake eats some food
            board.deleteFood()
            a = None
        if newPos in self.pSet:
            print("Returning -1")
            return -1 #This is for when the snake runs into itself
        self.pos.append(newPos)
        self.pSet.add(newPos)
        self.getNeck()
        return a  #It returns the tail position that was deleted to be used in Board.step()

    def changeDirection(self,newDir):
        if (newDir!=self.neck):
            self.dir = newDir

    def getKeyChange(self,keyString):
        try:
            self.changeDirection(self.stDic[keyString])
        except KeyError:
            return None


#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#

class Board:
    def __init__(self,size):
        self.size = size #constant. How many boxes will have each side of the board
        self.colisions = set()  #set of positions (2 dimension tuples) that are occupied by the snake body
        self.boxes = {} #Rectangle objets of the boxes that were drawn, for future undrawing
        self.foodPos = None
        #self.foodDrawing = None #For the rectangle object undrawing

    def drawBox(self,win,position,food=False):
        """Food for drawing a different color box."""
        sz = int(win.height / self.size)
        rec1 = Point(position[0]*sz , position[1]*sz)
        rec2 = Point((position[0]*sz)+sz , (position[1]*sz)+sz)
        box = Rectangle(rec1,rec2)
        if food:
            box.setFill(color_rgb(210,20,20)) #MAX 256
            box.setOutline(color_rgb(210,20,20))
        else:
            box.setFill(color_rgb(235,235,235)) #MAX 256
            box.setOutline(color_rgb(235,235,235))
            self.colisions.add(position)
        self.boxes[position] = box
        box.draw(win)
    
    def deleteFood(self):
        self.boxes[self.foodPos].undraw()
        self.foodPos = None
    
    def deleteBox(self,position):
        """self.boxes holds the current drawn boxes (as Rectangle objects)"""
        self.boxes[position].undraw()  
        self.boxes.pop(position)
        try:  #It also deletes the position from self.colisions
            self.colisions.remove(position)
        except KeyError:
            pass  #This is for when it deletes a food box, which isn't stored in self.colisions
    
    def doesColide(self,snk):
        headPos = snk.pos[-1]
        if (min(headPos) < 0) or (max(headPos) >= self.size):
            return True
        return False
        
    def step(self,win,snk):
        t = snk.step(self) #First it makes the move in theory
        if (t==None):
            self.spawnFood(win)
            self.drawBox(win,snk.pos[-1]) #Draws the move
            return True
        if (t!=-1 and (not self.doesColide(snk))): #This will be true if it didn't collide with anything
            self.deleteBox(t)  #Deletes the tail that was moved in snk.step()
            self.drawBox(win,snk.pos[-1]) #Draws the move
            return True
        return False
        
    def spawnFood(self,win):
        self.foodPos = (random.randint(0,self.size-1),random.randint(0,self.size-1))
        while self.foodPos in self.colisions:
            self.foodPos = (random.randint(0,self.size),random.randint(0,self.size))
        self.drawBox(win,self.foodPos,food=True)
            
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#
#________________________________________________________#

class InternalClock:
    dirKeys = {"flecha izquierda","flecha derecha","flecha arriba","flecha abajo"}
    def __init__(self,initialRate,initialAcc,initialPeriod):
        self.stepWait = initialRate
        self.acceleration = initialAcc
        self.period = initialPeriod
    
    def beat(self):
        keyboard.start_recording(recorded_events_queue=None)
        time.sleep(self.stepWait)
        pressedKeys = keyboard.stop_recording()
        for pK in reversed(pressedKeys):
            if pK.name in self.dirKeys:
                return pK.name