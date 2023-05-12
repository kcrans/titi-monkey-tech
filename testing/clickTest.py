#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo for psychopy.visual.ShapeStim.contains() and .overlaps()

Also inherited by various other stimulus types.
"""

from psychopy import visual, event, core

win = visual.Window(size=(800, 600), monitor='testmonitor', units='norm')
print(win.size)
mouse = event.Mouse()
txt = 'click the shape to quit\nscroll to adjust circle'
instr = visual.TextStim(win, text=txt, pos=(0, -.7), opacity=0.5)
msg = visual.TextStim(win, text=' ', pos=(0, -.4))


shape = visual.Rect(win, size=(0.5, 0.5))

# define a buffer zone around the mouse for proximity detection:
# use pix units just to show that it works to mix (shape and mouse use norm units)
bufzone = visual.Circle(win, radius=30, edges=13, units='pix')

# loop until detect a click inside the shape:

print(win.size)

while not mouse.isPressedIn(shape):
    instr.draw()
    # dynamic buffer zone around mouse pointer:
    bufzone.pos = mouse.getPos() * win.size / 2  # follow the mouse
    bufzone.size += mouse.getWheelRel()[1] / 20.0  # vert scroll adjusts radius
    # is the mouse inside the shape (hovering over it)?
    instr.text = f'Mouse: {mouse.getPos()}'
    msg.text = f'Buffer: {bufzone.pos}'
    bufzone.draw()  # drawing helps visualize the mechanics
    msg.draw()
    shape.draw()
    win.flip()

win.close()
core.quit()

# The contents of this file are in the public domain.
