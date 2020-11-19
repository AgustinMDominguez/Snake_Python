from graphics import *
import keyboard
import time

"""windowSize = 500
mainWin = GraphWin("Snake", windowSize, windowSize)
a = Rectangle(Point(200,200),Point(300,300))
a.draw(mainWin)
mainWin.getMouse() # Pause to view result
mainWin.close()    # Close window when done"""

#recorded = keyboard.record(until='esc')
#for a in recorded:
#    print(a,a.name,"\n")

print("Starting:\n")
keyboard.start_recording(recorded_events_queue=None)
time.sleep(2)
a = keyboard.stop_recording()
for e in a:
    print(e.name,type(e.name))