#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice, shuffle # for randomness in the display of stimuli
import numpy as np

from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio

from init import mywin, trial_start_sound, click_sound, neg_reinforce_sound, kb, InputTracker, hor_scale, scale, get_shape


def run_experiment(record_data, shape_name_1, shape_name_2, parameters, experiment_parameters):
    """
    Start an experiment phase.
    
    Keyword arguments:
    record_data -- function that writes data to file
    shape_name_1 -- name of positive stimuli shape
    shape_name_2 -- name of negative stimuli shape
    parameters -- dict of common parameters
    experiment_parameters -- parameters exclusive to experiment phase
    """
    # Parameters
    negative_reinforcement_delay = parameters["negative_reinforcement_delay"]
    positive_reinforcement_delay = parameters["positive_reinforcement_delay"]
    hold_phase_delay = parameters["hold_phase_delay"]
    shape_size = parameters["shape_size"]
    pos_duration = parameters["pos_duration"] # How long to wait when positive stimuli is presented
    neg_duration = parameters["neg_duration"] # Ditto for negative stimuli
    num_pos = experiment_parameters["num_pos"] # Number of go signal trials
    num_neg = experiment_parameters["num_neg"] # Number of no-go signal trials
    
    #create positive stimuli
    pos_stim = get_shape(shape_name_1)
        
    #create negative stimuli
        
    neg_stim = get_shape(shape_name_2)
    
    # An array of strings representing different stimuli shapes
    stimStringList = [shape_name_1]*num_pos + [shape_name_2]*num_neg
    shuffle(stimStringList) # Shuffle to make the order random
    # Turn it into an array of dicts, which is the proper format for
    # TrialHandler
    stimList = [{'shape': string} for string in stimStringList]
    trials = data.TrialHandler(stimList, nReps = 1)
    device = InputTracker()
    shapes = {shape_name_1: pos_stim, shape_name_2: neg_stim} # 
    i = 0 # Tracks trial number
    keys = kb.getKeys()
    hor_pos = 0.5*(hor_scale/2) # How far to go horizontally on the left and right
    
    trial_results = []
    
    globalClock = core.Clock()
    trialClock = core.Clock()
    for this_trial in trials:
        keys = kb.getKeys()
        shape_str = this_trial['shape']
        dis_shape = shapes[shape_str]
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
        if shape_str == shape_name_1: # If it is displaying a go stimulus
            touched = False
            while trialClock.getTime() < pos_duration:
                keys = kb.getKeys()
                if 'escape' in keys:
                    trials.finished = True
                    return False
                event.clearEvents()
                dis_shape.draw()
                mywin.flip()
                if device.is_touched():
                    touched = True
                    if dis_shape.contains(scale*touch_tracker.getPos()):
                        trial_results.append([i + 1, False, True, trialClock.getTime(), touch_count, True, shape_size])
                        click_sound.play()
                        mywin.flip()
                        core.wait(positive_reinforcement_delay)
                    else:
                        trial_results.append([i + 1, False, True, trialClock.getTime(), touch_count, False, shape_size])
                        neg_reinforce_sound.play()
                        mywin.flip()
                        core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
            if not touched:
                trial_results.append([i + 1, False, False, trialClock.getTime(), touch_count, False, shape_size])
        else: # If a negative stimulus is displayed
            while True:
                keys = kb.getKeys()
                if 'escape' in keys:
                    trials.finished = True
                    return False
                if trialClock.getTime() >= neg_duration:
                    trial_results.append([i + 1, True, False, trialClock.getTime(), touch_count, False, shape_size])
                    click_sound.play()
                    mywin.flip()
                    core.wait(positive_reinforcement_delay)
                    break
                event.clearEvents()
                dis_shape.draw()
                mywin.flip()
                if device.is_touched():
                    trial_results.append([i + 1, True, True, trialClock.getTime(), touch_count, False, shape_size])
                    neg_reinforce_sound.play()
                    mywin.flip()
                    core.wait(negative_reinforcement_delay)
                    break # Break out of inner loop if anywhere on screen is touched
        i += 1
    for trial in trial_results:
        record_data(*trial)    
    return True
