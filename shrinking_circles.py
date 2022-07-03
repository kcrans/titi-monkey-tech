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

#create a mouse event class to track touch input
touch_tracker = event.Mouse(visible=True, win=mywin)

click_sound = Sound('clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('negativeReinforcement.wav', name='negsound')

#create circle stimuli
circle = visual.ShapeStim(
    win=mywin, name='go_circle',
    size=0.8, vertices='circle',
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
    print('shrinking')
    width = shape.size[0]
    if width > 0:
        new_size = width - 0.05
        shape.size = (new_size, new_size)
    #hit_count = 0

def grow(shape):
    print('growing')
    width= shape.size[0]
    if width < 0.9:
        new_size = width + 0.05
        shape.size = (new_size, new_size)
    #miss_count = 0
    
def my_contains(polygon, x, y):
    radius_sqrd = (polygon.size[0])**2
    if x**2 + y**2 <= radius_sqrd:
        return True
    else:
        return False

while globalClock.getTime() < session_timeout_time:
    event.clearEvents()
    circle.draw()
    mywin.update()
    touch_tracker.clickReset() 
    if touch_tracker.getPressed(getTime=True)[0][0] == 1: #and click_sound.status != 'STARTED' and neg_reinforce_sound.status != 'STARTED'
        click_sound.stop() # Stop sounds early if another click is registered
        neg_reinforce_sound.stop() #
        if my_contains(circle, *touch_tracker.getPos()):
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
        elif miss_count == 3:
            grow(circle)
            miss_count = 0
        core.wait(touch_delay)

