#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np

session_timeout_time = 60
touch_delay = 0.25

mon = monitors.Monitor('macbook')
print(prefs.general['winType'])
#[500, 500]
#create a window
mywin = visual.Window(size=[1440, 900], fullscr=False, color="black", monitor=mon, units="height")
#mywin.monitor.setCurrent('macbook.json')
upper_bound = 0.9
lower_bound = 0
start = 0.8
increment = 0.05

#create a mouse event class to track touch input
touch_tracker = event.Mouse(visible=True, win=mywin)

click_sound = Sound('clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('negativeReinforcement.wav', name='negsound')

#create circle stimuli
circle = visual.ShapeStim(
    win=mywin, name='go_circle',
    size=start, vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)
    
txt = 'click the shape to quit\nscroll to adjust circle'
instr = visual.TextStim(mywin, text=txt, pos=(-1.0, -.7), opacity=0.5)

globalClock = core.Clock()
starttime = globalClock.getTime()
trialClock = core.Clock()

hit_count = 0
miss_count = 0


def shrink(shape):
    width = shape.size[0]
    if width > lower_bound:
        new_size = width - increment
        shape.size = (new_size, new_size)
    #hit_count = 0

def grow(shape):
    width= shape.size[0]
    if width < upper_bound:
        new_size = width + increment
        shape.size = (new_size, new_size)
    #miss_count = 0
    
def my_contains(polygon, x, y):
    radius_sqrd = (polygon.size[0])**2
    print(x, y, polygon.size[0])
    if x**2 + y**2 <= radius_sqrd:
        return True
    else:
        return False
def not_equal(pos1, pos2):
    if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
        return True
    else:
        return False
circle.draw()
mywin.update()
lastPos = touch_tracker.getPos()
while globalClock.getTime() < session_timeout_time:
    event.clearEvents()
    if not_equal(touch_tracker.getPos(), lastPos): #and click_sound.status != 'STARTED' and neg_reinforce_sound.status != 'STARTED'
        lastPos = touch_tracker.getPos()
        click_sound.stop()
        neg_reinforce_sound.stop()
        if my_contains(circle, *lastPos):
            click_sound.play()
            #print('in')
            hit_count += 1
            miss_count = 0
        else:
            neg_reinforce_sound.play()
            #print('out')
            miss_count += 1
            hit_count = 0
        if hit_count == 3:
            shrink(circle)
            hit_count = 0
            circle.draw()
            mywin.update()
        elif miss_count == 3:
            grow(circle)
            miss_count = 0
            circle.draw()
            mywin.update()
        core.wait(touch_delay)

