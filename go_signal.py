#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np
from init import mywin, touch_tracker, trial_start_sound, click_sound, neg_reinforce_sound, kb, input_tracker, hor_scale


def normal_training(record_data, new_shape, session_timeout_time, parameters):
    # Parameters
    negative_reinforcement_delay = float(parameters["negative_reinforcement_delay"])
    positive_reinforcement_delay = float(parameters["positive_reinforcement_delay"])
    hold_phase_delay = float(parameters["hold_phase_delay"])
    circle_diam = float(parameters["circle_diam"])
    pos_duration = float(parameters["pos_duration"]) # How long to wait when positive stimuli is presented
    neg_duration = float(parameters["neg_duration"]) # Ditto for negative stimuli
    
        #create circle stimuli
    circle = visual.ShapeStim(
        win=mywin, name='go_circle',
        size=(circle_diam, circle_diam), vertices='circle',
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=0.0,     colorSpace='rgb', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
        
    #create triangle stimuli
        
    triangle = visual.Polygon(
        win=mywin, edges=3, size=(1, 1),
        anchor='center', pos=(0.3, 0),
        fillColor='grey', name='stop_triangle'
        )
    
    device = input_tracker()
    shapes = [circle, triangle] # 
    i = 0 # Tracks trial number
    hor_pos = (hor_scale/2) - 0.4 # How far to go horizontally on the left and right
    globalClock = core.Clock()
    #starttime = globalClock.getTime() # depreciated
    trialClock = core.Clock()
    while globalClock.getTime() < session_timeout_time - 6.0:
        index = new_shape(i)
        dis_shape = shapes[index]
        mywin.flip()
        side = choice((-1, 1))
        dis_shape.pos = (side*(hor_pos - index*0.1), index*-.125)
        trial_start_sound.play()
        touch_down = False
        touch_count = 0
        trialClock.reset()
        while trialClock.getTime() < hold_phase_delay:
            if device.is_touched():
                if not touch_down:
                    touch_count += 1
                    touch_down = True
            else:
                touch_down = False
            
        trialClock.reset()
        if index == 0: # If a go circle is being displayed
            touched = False
            while trialClock.getTime() < pos_duration and globalClock.getTime() < session_timeout_time:
                event.clearEvents()
                dis_shape.draw()
                mywin.update()
                if device.is_touched():
                    touched = True
                    if dis_shape.contains(touch_tracker):
                        record_data(i + 1, 'FALSE', 'TRUE', trialClock.getTime(), touch_count, 'TRUE', circle_diam)
                        click_sound.play()
                        mywin.flip()
                        core.wait(positive_reinforcement_delay)
                    else:
                        record_data(i + 1, 'FALSE', 'TRUE', trialClock.getTime(), touch_count, 'FALSE', circle_diam)
                        neg_reinforce_sound.play()
                        mywin.flip()
                        core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
            if not touched:
                record_data(i + 1, 'FALSE', 'FALSE', trialClock.getTime(), touch_count, 'FALSE', circle_diam)
        else: # If a no-go triangle is being displayed
            while globalClock.getTime() < session_timeout_time:
                if trialClock.getTime() >= neg_duration:
                    record_data(i + 1, 'TRUE', 'FALSE', trialClock.getTime(), touch_count, 'FALSE', circle_diam)
                    click_sound.play()
                    mywin.flip()
                    core.wait(positive_reinforcement_delay)
                    break
                event.clearEvents()
                dis_shape.draw()
                mywin.update()
                if device.is_touched():
                    record_data(i + 1, 'TRUE', 'TRUE', trialClock.getTime(), touch_count, 'FALSE', circle_diam)
                    neg_reinforce_sound.play()
                    mywin.flip()
                    core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
        i += 1
