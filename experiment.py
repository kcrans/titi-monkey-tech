#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice, shuffle # for randomness in the display of stimuli
import numpy as np
from init import mywin, touch_tracker, trial_start_sound, click_sound, neg_reinforce_sound, input_tracker, hor_scale


# Parameters
negative_reinforcement_delay = 3.0
positive_reinforcement_delay = 1.0
hold_phase_delay = 2
session_timeout_time = 30 # Normallly 480.0 seconds
circle_diam = 0.8
neg_response_time = 2.0 # How long to wait when negative stimuli is presented

num_pos = 2 # Number of go signal trials
num_neg = 4 # Number of no-go signal trials


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

def run_experiment(record_data):
    # An array of strings representing different stimuli shapes
    stimStringList = ['circle']*num_pos + ['triangle']*num_neg
    shuffle(stimStringList) # Shuffle to make the order random
    # Turn it into an array of dicts, which is the proper format for
    # TrialHandler
    stimList = [{'shape': string} for string in stimStringList]
    trials = data.TrialHandler(stimList, nReps = 1)
    device = input_tracker()
    shapes = {'circle': circle, 'triangle': triangle} # 
    i = 0 # Tracks trial number
    hor_pos = (hor_scale/2) - 0.4 # How far to go horizontally on the left and right
    globalClock = core.Clock()
    #starttime = globalClock.getTime() # depreciated
    trialClock = core.Clock()
    convert = {'circle':0, 'triangle':1}
    for this_trial in trials:
        shape_str = this_trial['shape']
        dis_shape = shapes[shape_str]
        mywin.flip()
        side = choice((-1, 1))
        index = convert[shape_str]
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
        if shape_str == 'circle': # If it is displaying a go stimulus
            touched = False
            while trialClock.getTime() < 30.0 and globalClock.getTime() < session_timeout_time:
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
        else: # If a negative stimulus is displayed
            while globalClock.getTime() < session_timeout_time:
                if trialClock.getTime() >= neg_response_time:
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
    return