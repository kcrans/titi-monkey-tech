#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from psychopy.hardware import keyboard
import numpy as np
from init import mywin, scale, touch_tracker, click_sound, neg_reinforce_sound, kb, input_tracker

def circle_run(record_data, session_timeout_time, parameters):
    # Go signal training parameters
    touch_delay = float(parameters["touch_delay"]) # How long until new touches can be registered after a touch
    start = float(parameters["start"]) # Start with a specified diameter
    upper_bound = float(parameters["upper_bound"])
    lower_bound = float(parameters["lower_bound"])
    increment = float(parameters["increment"])
    
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
    
    hit_count = 0
    miss_count = 0
    
    device = input_tracker()

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
        if device.is_touched():
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
                record_data(trial, 'FALSE', 'TRUE', trial_time, 0, 'TRUE', circle.size[0])
            else:
                neg_reinforce_sound.play()
                miss_count += 1
                hit_count = 0
                trial += 1
                record_data(trial, 'FALSE', 'TRUE', trial_time, 0, 'FALSE', circle.size[0])
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
        parameters["start"] = circle.size[0]
        return True
