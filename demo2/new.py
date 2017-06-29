#Created on 15-06-2017
#Author = Valtteri Koskivuori (vkoskiv)
#Version 0.2

import RPi.GPIO as gp
import time

#setup
gp.setmode(gp.BCM)

cG = 17
cY = 27
cR = 22

pG = 16
pR = 20
pY = 21

btn = 26
mvmt = 4

#seconds for forced light change
forceChange = 15

gp.setup(btn, gp.IN)
gp.setup(mvmt, gp.IN)
gp.setup(cG, gp.OUT)
gp.setup(cY, gp.OUT)
gp.setup(cR, gp.OUT)
gp.setup(pG, gp.OUT)
gp.setup(pR, gp.OUT)
gp.setup(pY, gp.OUT)

#funcs
def reset():
    gp.output(cG, 1)
    gp.output(cY, 0)
    gp.output(cR, 0)
    gp.output(pG, 0)
    gp.output(pR, 1)
    gp.output(pY, 0)

def seq():
    time.sleep(1)
    gp.output(pY, 1)
    gp.output(cG, 0)
    gp.output(cY, 1)
    time.sleep(1)
    gp.output(cY, 0)
    gp.output(cR, 1)
    time.sleep(1)
    gp.output(pY, 0)
    gp.output(pR, 0)
    gp.output(pG, 1)
    time.sleep(3)
    gp.output(pG, 0)
    gp.output(pR, 1)
    time.sleep(1)
    gp.output(cR, 0)
    gp.output(cY, 1)
    time.sleep(1)
    gp.output(cY, 0)
    gp.output(cG, 1)
    time.sleep(2)

#logic
reset()

clicked = False

while True:
    instate = gp.input(btn)
    mvstate = gp.input(mvmt)
    if instate == gp.HIGH:
        maxWait = time.time() + forceChange
        clicked = True
    else:
        if clicked:
            if mvstate == gp.LOW:
                clicked = False
                seq()
            if mvstate == gp.HIGH and time.time() >= maxWait:
                clicked = False
                seq()
            if mvstate == gp.HIGH and time.time() < maxWait:
                print("Await motion")
            else:
                print("no clicc")
                reset()
#Cleanup
gp.cleanup()
