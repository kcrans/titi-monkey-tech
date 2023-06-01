#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module to run the first experiment: circle stimuli training. Used to teach
the monkeys how to click on stimuli shown on the display.
"""

from psychopy import visual, core, event  # import some basic libraries from PsychoPy

from init import mywin, scale, click_sound, neg_reinforce_sound, kb, InputTracker

def circle_run(record_data, session_timeout_time, parameters):
    """
    Input: function to record data, time limit, and session parameters
    
    Output: 
        True if experiment succesfully run
        False if ended early by hitting the escape key
    """
    # Go signal training parameters
    touch_delay = parameters["touch_delay"] # How long until new touches can be registered after a touch
    start = parameters["start"] # Start with a specified diameter
    upper_bound = parameters["upper_bound"]
    lower_bound = parameters["lower_bound"]
    increment = parameters["increment"]

        # Create circle stimuli object
    circle = visual.ShapeStim(
        win=mywin, name='go_circle',
        size=start, vertices='circle',
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=0.0,     colorSpace='rgb', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)

    def shrink(shape):
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
        radius_sqrd = (0.5*polygon.size[0])**2
        if (scale*x)**2 + (scale*y)**2 <= radius_sqrd:
            print(polygon.size[0])
            return True
        # Else if located outside circle radius
        return False

    def not_equal(pos1, pos2):
        if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
            return True
        # Else if (x1, y1) == (x2, y2)
        return False

    hit_count = 0
    miss_count = 0

    device = InputTracker()
    
    keys = kb.getKeys()
    circle.draw()
    mywin.flip()
    last_pos = device.getPos()

    global_clock = core.Clock() # Time elapsed since experiment began
    trial_clock = core.Clock()  # Trial time, resets each trial

    trial_results = []
    trial = 0
    while global_clock.getTime() < session_timeout_time and 'escape' not in keys:
        event.clearEvents()
        keys = kb.getKeys()
        if device.is_touched():
            last_pos = device.getPos() # Get the position of the touch
            trial_time = trial_clock.getTime() # Record the time since last touch
            trial_clock.reset()
            click_sound.stop() # Stop the sounds if they are still playing
            neg_reinforce_sound.stop()
            if quick_contains(circle, *last_pos):
                click_sound.play()
                hit_count += 1
                miss_count = 0
                trial += 1
                trial_results.append([trial, False, True, trial_time, 0, True, circle.size[0]])
            else:
                neg_reinforce_sound.play()
                miss_count += 1
                hit_count = 0
                trial += 1
                trial_results.append([trial, False, True, trial_time, 0, False, circle.size[0]])
            if hit_count == 3:
                shrink(circle)
                hit_count = 0
                circle.draw()
                mywin.flip()
            elif miss_count == 3:
                grow(circle)
                miss_count = 0
                circle.draw()
                mywin.flip()
            core.wait(touch_delay)
    if 'escape' in keys:
        return False
    # Else store the circle size and trial results
    parameters["start"] = circle.size[0]
    for trial in trial_results:
        record_data(*trial)
    return True
