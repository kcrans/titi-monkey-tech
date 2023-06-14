#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for run phases 2 - 4 of training:
"""
from random import choice # for randomness in the display of stimuli

from psychopy import core, event

from init import mywin, trial_start_sound, click_sound, neg_reinforce_sound
from init import kb, InputTracker, hor_scale, scale, get_shape

def normal_training(debug, record_data, new_shape, session_timeout_time,
shape_name_1, shape_name_2, parameters):
    """
    Start a training phase.
    
    Keyword arguments:
    record_data -- function that writes data to file
    session_timeout_time -- max length of experiment in seconds
    new_shape -- function that returns the index of the shape array to use
    in a trial. This differentiates the stages. I.e. 
    shape_name_1 -- name of positive stimuli shape
    shape_name_2 -- name of negative stimuli shape
    parameters -- dict of common parameters for phases 1-3
    """
    for param in parameters.keys():
        print(type(parameters[param]))
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

    device = InputTracker()
    shapes = [pos_stim, neg_stim] # List of stimuli 1 and 2
    trial = 1 # Tracks trial number
    hor_pos = 0.5*(hor_scale/2) # How far to go horizontally on the left and right

    keys = kb.getKeys()

    # Amount of time theoritically needed to complete a trial.
    # Can be used to exit early if there isn't enough time to complete
    # a new trial.
    time_needed = hold_phase_delay + max(pos_duration, neg_duration)
    # Or just be OK with going "overtime"
    time_needed = 0

    trial_results = []

    global_clock = core.Clock() # Time during whole run
    trial_clock = core.Clock() # Time during trial
    while global_clock.getTime() < session_timeout_time - time_needed:
        index = new_shape(trial - 1) # index = 0 or 1
        dis_shape = shapes[index] # get the shape based off new_shape()
        mywin.flip() # Clear framebuffer
        side = choice((-1, 1)) # Random
        dis_shape.pos = (side*hor_pos, 0)
        trial_start_sound.play()
        touch_down = False
        touch_count = 0
        trial_clock.reset()
        while trial_clock.getTime() < hold_phase_delay:
            if 'escape' in kb.getKeys():
                mywin.close()
                core.quit()
                return False
            if device.is_touched():
                if not touch_down:
                    touch_count += 1
                    touch_down = True
            else:
                touch_down = False

        trial_clock.reset()
        if index == 0: # If a go stimuli is being displayed
            touched = False
            while trial_clock.getTime() < pos_duration:
                keys = kb.getKeys()
                if 'escape' in keys:
                    mywin.close()
                    core.quit()
                    return False
                event.clearEvents()
                dis_shape.draw()
                mywin.flip()
                if device.is_touched():
                    touched = True
                    if dis_shape.contains(scale*device.getPos()):
                        trial_results.append([trial, False, True,
                        trial_clock.getTime(), touch_count, True, shape_size])
                        click_sound.play()
                        mywin.flip()
                        core.wait(positive_reinforcement_delay)
                    else:
                        trial_results.append([trial, False, True,
                        trial_clock.getTime(), touch_count, False, shape_size])
                        neg_reinforce_sound.play()
                        mywin.flip()
                        core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
            if not touched:
                trial_results.append([trial, 'FALSE', 'FALSE',
                trial_clock.getTime(), touch_count, 'FALSE', shape_size])
                neg_reinforce_sound.play()
                mywin.flip()
                core.wait(negative_reinforcement_delay)
        else: # If a no-go stimuli is being displayed
            while True:
                keys = kb.getKeys()
                if 'escape' in keys:
                    mywin.close()
                    core.quit()
                    return False
                if trial_clock.getTime() >= neg_duration:
                    trial_results.append([trial, 'TRUE', 'FALSE',
                    trial_clock.getTime(), touch_count, 'FALSE', shape_size])
                    click_sound.play()
                    mywin.flip()
                    core.wait(positive_reinforcement_delay)
                    break
                event.clearEvents()
                dis_shape.draw()
                mywin.flip()
                if device.is_touched():
                    trial_results.append([trial, 'TRUE', 'TRUE',
                    trial_clock.getTime(), touch_count, 'FALSE', shape_size])
                    neg_reinforce_sound.play()
                    mywin.flip()
                    core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
        trial += 1
    for trial in trial_results:
        record_data(*trial)
    mywin.close()
    core.quit()
    return True
