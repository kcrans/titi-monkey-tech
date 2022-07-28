#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from psychopy.hardware import keyboard
import numpy as np
from init import mywin, scale, touch_tracker, click_sound, neg_reinforce_sound, kb, touch_tracker, is_touched


# Go signal training parameters
session_timeout_time = 60
touch_delay = 0.25 # How long untill new touches can be regestired registered
start = 0.8 # Start with a diameter that is 80% of screen height
upper_bound = 0.9
lower_bound = 0
increment = 0.05

# Create circle stimuli object
circle = visual.ShapeStim(
    win=mywin, name='go_circle',
    size=start, vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

def shrink(shape): # Modify so no arguements are needed
    radius = shape.size[0]
    if radius > lower_bound:
        new_radius = radius - increment
        shape.size = (new_radius, new_radius)
        #hit_count = 0

def grow(shape):
    radius = shape.size[0]
    if radius < upper_bound:
        new_radius = radius + increment
        shape.size = (new_radius, new_radius)
        #miss_count = 0

    # Function to see if touches are in the circle.
    # Uses the fact that circles are the only shape in this program
def quick_contains(polygon, x, y): 
    radius_sqrd = (scale*polygon.size[0])**2
    if x**2 + y**2 <= radius_sqrd:
        return True
    else:
        return False
            
def not_equal(pos1, pos2):
    if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
        return True
    else:
        return False

def circle_run(record_data):
    hit_count = 0
    miss_count = 0

    keys = kb.getKeys()
    circle.draw()
    mywin.update()
    lastPos = touch_tracker.getPos()

    globalClock = core.Clock() # Time elapsed since experiment began
    trialClock = core.Clock()  # Trial time, resets each trial
    
    trial = 0
    while globalClock.getTime() < session_timeout_time and 'escape' not in keys: # Reorder so timing makes sense
        event.clearEvents()
        keys = kb.getKeys()
        if is_touched():
            lastPos = touch_tracker.getPos() # Get the position of the touch
            trial_time = trialClock.getTime() # Record the time since last touch
            trialClock.reset()
            click_sound.stop() # Stop the sounds if they are still playing
            neg_reinforce_sound.stop()
            if quick_contains(circle, *lastPos):
                click_sound.play()
                hit_count += 1
                miss_count = 0
                trial += 1
                record_data(trial, 'FALSE', 'TRUE', trial_time, 'TRUE', 0, circle.size[0])
            else:
                neg_reinforce_sound.play()
                miss_count += 1
                hit_count = 0
                trial += 1
                record_data(trial, 'FALSE', 'TRUE', trial_time, 'FALSE', 0, circle.size[0])
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
    if 'escape' in keys:
        return False
    else:
        return True
