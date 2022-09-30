from psychopy import visual, core, event, monitors, prefs, gui  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np
from init import mywin, touch_tracker, trial_start_sound, click_sound, neg_reinforce_sound, kb, input_tracker, hor_scale

circle_diam = 0.8

#create circle stimuli
circle = visual.ShapeStim(
    win=mywin, name='go_circle',
    size=(circle_diam - 0.1, circle_diam - 0.1), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb', fillColor='red',
    opacity=None, interpolate=True)
    
#create triangle stimuli
    
triangle = visual.Polygon(
    win=mywin, edges=3, size=(1, 1),
    anchor='center', pos=(0.3, 0),
    fillColor='grey', name='stop_triangle'
    )

square = visual.rect.Rect(
    win=mywin, size = (0.7,0.7), pos=(0,0),
    fillColor='white', name = "stop_square"
    )

cross_vertices = [
    (-0.1, +0.4),  # up
    (+0.1, +0.4),
    (+0.1, +0.1),
    (+0.4, +0.1),  # right
    (+0.4, -0.1),
    (+0.1, -0.1),
    (+0.1, -0.4),  # down
    (-0.1, -0.4),
    (-0.1, -0.1),
    (-0.4, -0.1),  # left
    (-0.4, +0.1),
    (-0.1, +0.1),
]

cross = visual.ShapeStim(
    win=mywin, name='go_cross',
    size=(1, 1), vertices=cross_vertices,
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb', fillColor='grey',
    opacity=None, interpolate=True)
    
star_points = [
    (0.0, 0.5),
    (0.1123, 0.1545),
    (0.4755, 0.1545),
    (0.1816, -0.059),
    (0.2939, -0.4045),
    (0, -0.191),
    (-0.2939, -0.4045),
    (-0.1816, -0.059),
    (-0.4755, 0.1545),
    (-0.1123, 0.1545)
]
# Maybe shift so it doesn't look like there is more 
    
star = visual.ShapeStim(
    win=mywin, name='go_cross',
    size=(1, 1), vertices=star_points,
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb', fillColor='grey',
    opacity=None, interpolate=True)
    
strike_mask = visual.ShapeStim(
    win=mywin, name='go_circle',
    size=(circle_diam, circle_diam), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0, opacity=0.0, interpolate=True)
    
strike_circle = visual.ImageStim(win=mywin, image='assets/goSignal_strike.png', size = (0.8, 0.8))
test = strike_circle.draw
def func1():
    test()
    circle.draw()
strike_circle.draw = func1

print(triangle.units, square.units, cross.units, star.units, strike_circle.units)
mywin.flip()
strike_circle.draw()
#circle.draw()
mywin.update()
core.wait(3)