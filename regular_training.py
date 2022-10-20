#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np
from init import mywin, touch_tracker, trial_start_sound, click_sound, neg_reinforce_sound, kb, input_tracker, hor_scale, scale, get_shape


def normal_training(record_data, new_shape, session_timeout_time, shape_name_1, shape_name_2, parameters):
    """
    Start a training phase.
    
    Keyword arguments:
    record_data -- function that writes data to file
    session_timeout_time -- max length of experiment in seconds
    shape_name_1 -- name of positive stimuli shape
    shape_name_2 -- name of negative stimuli shape
    parameters -- dict of common parameters for phases 1-3
    """
    # Parameters
    negative_reinforcement_delay = parameters["negative_reinforcement_delay"]
    positive_reinforcement_delay = parameters["positive_reinforcement_delay"]
    hold_phase_delay = parameters["hold_phase_delay"]
    shape_size = parameters["shape_size"]
    pos_duration = parameters["pos_duration"] # How long to wait when positive stimuli is presented
    neg_duration = parameters["neg_duration"] # Ditto for negative stimuli
    
    #create positive stimuli
    pos_stim = get_shape(shape_name_1)
        
    #create negative stimuli
        
    neg_stim = get_shape(shape_name_2)
    
    device = input_tracker()
    shapes = [pos_stim, neg_stim] # 
    i = 0 # Tracks trial number
    hor_pos = 0.5*(hor_scale/2) # How far to go horizontally on the left and right
    
    keys = kb.getKeys()
    time_needed = hold_phase_delay + max(pos_duration, neg_duration)
    time_needed = 4
    globalClock = core.Clock()
    trialClock = core.Clock()
    while globalClock.getTime() < session_timeout_time - time_needed:
        index = new_shape(i)
        dis_shape = shapes[index]
        mywin.flip()
        side = choice((-1, 1))
        dis_shape.pos = (side*hor_pos, 0)
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
        if index == 0: # If a go stimuli is being displayed
            touched = False
            while trialClock.getTime() < pos_duration:
                keys = kb.getKeys()
                if 'escape' in keys:
                    return
                event.clearEvents()
                dis_shape.draw()
                mywin.update()
                if device.is_touched():
                    touched = True
                    if dis_shape.contains(scale*touch_tracker.getPos()):
                        record_data(i + 1, 'FALSE', 'TRUE', trialClock.getTime(), touch_count, 'TRUE', shape_size)
                        click_sound.play()
                        mywin.flip()
                        core.wait(positive_reinforcement_delay)
                    else:
                        record_data(i + 1, 'FALSE', 'TRUE', trialClock.getTime(), touch_count, 'FALSE', shape_size)
                        neg_reinforce_sound.play()
                        mywin.flip()
                        core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
            if not touched:
                record_data(i + 1, 'FALSE', 'FALSE', trialClock.getTime(), touch_count, 'FALSE', shape_size)
        else: # If a no-go stimuli is being displayed
            while True:
                keys = kb.getKeys()
                if 'escape' in keys:
                    return
                if trialClock.getTime() >= neg_duration:
                    record_data(i + 1, 'TRUE', 'FALSE', trialClock.getTime(), touch_count, 'FALSE', shape_size)
                    click_sound.play()
                    mywin.flip()
                    core.wait(positive_reinforcement_delay)
                    break
                event.clearEvents()
                dis_shape.draw()
                mywin.update()
                if device.is_touched():
                    record_data(i + 1, 'TRUE', 'TRUE', trialClock.getTime(), touch_count, 'FALSE', shape_size)
                    neg_reinforce_sound.play()
                    mywin.flip()
                    core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
        i += 1
