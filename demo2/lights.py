#Created on 15-06-2017
#Author = Valtteri Koskivuori (vkoskiv)
#Version 0.1

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

gp.setup(btn, gp.IN)
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

while True:
    instate = gp.input(btn)
    if instate == gp.HIGH:
        seq()
        break
    else:
        reset()

#Cleanup
gp.cleanup()
