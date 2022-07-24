#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo for psychopy.visual.ShapeStim.contains() and .overlaps()
Also inherited by various other stimulus types.
"""

from psychopy import visual, event, core

win = visual.Window(size=(500, 500), monitor='testMonitor', units='norm')
mouse = event.Mouse()
txt = 'click the shape to quit\nscroll to adjust circle'
instr = visual.TextStim(win, text=txt, pos=(0, -.7), opacity=0.5)
msg = visual.TextStim(win, text=' ', pos=(0, -.4))

globalClock = core.Clock()

# a target polygon (strange shape):
shape = visual.Rect(win, fillColor='black')

# define a buffer zone around the mouse for proximity detection:
# use pix units just to show that it works to mix (shape and mouse use norm units)
bufzone = visual.Circle(win, radius=0.3, edges=13, units='norm')

# loop until detect a click inside the shape:
while not mouse.isPressedIn(shape) and globalClock.getTime() <  60:
    instr.draw()
    # dynamic buffer zone around mouse pointer:
    pos = mouse.getPos()
    bufzone.pos = (pos[0]/2.0, pos[1]/2.0) # follow the mouse
    bufzone.size += mouse.getWheelRel()[1] / 20.0  # vert scroll adjusts radius
    # is the mouse inside the shape (hovering over it)?
    instr.text = str(mouse.getPressed())
    msg.text = str(event.getKeys())
    core.wait(0.25)
    bufzone.draw()  # drawing helps visualize the mechanics
    msg.draw()
    shape.draw()
    win.flip()

win.close()
core.quit()
