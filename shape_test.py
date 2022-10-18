from psychopy import visual, core, event, monitors, prefs, gui  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np
from init import mywin, touch_tracker, trial_start_sound, click_sound, neg_reinforce_sound, kb, input_tracker, scale, hor_scale

circle_diam = 0.8

shape_scale = 0.6

def get_shape(mywin, shape_name):
    #create circle stimuli
    if shape_name == 'circle':
        circle = visual.ShapeStim(
            win=mywin, name='go_circle',
            size=(shape_scale, shape_scale), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0,     colorSpace='rgb', fillColor='white',
            opacity=None, interpolate=True)
        return circle
    #create triangle stimuli
    elif shape_name == 'triangle':    
        triangle = visual.Polygon(
            win=mywin, edges=3, size=(shape_scale, shape_scale),
             pos=(0, -0.1),
            fillColor='grey', name='stop_triangle'
            )
        return triangle
    elif shape_name == 'square':
        square = visual.rect.Rect(
            win=mywin, size = (shape_scale- 0.1, shape_scale - 0.1), pos=(0,0),
            fillColor='white', name = "stop_square"
            )
        return square
    elif shape_name == 'cross':
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
            size=(shape_scale, shape_scale), vertices=cross_vertices,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0,     colorSpace='rgb', fillColor='grey',
            opacity=None, interpolate=True)
            
        return cross
    elif shape_name == 'star':
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
        # Maybe shift so it doesn't look like there is more space on the bottom
        star = visual.ShapeStim(
            win=mywin, name='star',
            size=(shape_scale, shape_scale), vertices=star_points,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0,     colorSpace='rgb', fillColor='grey',
            opacity=None, interpolate=True)
        
        return star
    elif shape_name == 'strike_circle':
        # Add an invisible circle in order to track touches
        strike_mask = visual.ShapeStim(
            win=mywin, name='go_circle',
            size=(shape_scale, shape_scale), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0, opacity=0.0, interpolate=True)
            
        strike_circle = visual.ImageStim(win=mywin, image='assets/goSignal_strike.png', size = (shape_scale, shape_scale))
        visible_draw = strike_circle.draw
        def new_draw():
            visible_draw()
            strike_mask.draw()
        strike_circle.draw = new_draw
        return strike_circle
    else:
        return None

shapes = [get_shape(mywin, shape_str) for shape_str in ['circle', 'triangle', 'square', 'cross', 'star', 'strike_circle' ]] # 
shape_index = 0
def move_index(index):
    if index > 5:
        index = 0
    if index < 0:
        index = 5
    return index

def change_size(new_size):
    for shape in shapes:
        shape.size = (new_size, new_size)

hor_pos = 0.5*(hor_scale/2) # How far to go horizontally on the left and right
print(hor_scale, hor_pos)


keys = kb.getKeys()
side = -1

msg = visual.TextStim(mywin, text=' ', pos=(0.0, 0.0), color = (1.0, 0.0, 0.0), height= 0.05)
controls = visual.TextStim(mywin, text='w, s: cycle through shapes\na, d: change size                ', pos=(-1*hor_pos, -0.4), color = (1.0, 0.0, 0.0), height= 0.05)
mywin.flip()
device = input_tracker()
while 'escape' not in keys:
    dis_shape = shapes[shape_index]
    event.clearEvents()
    keys = kb.getKeys()
    if keys:
        for k in keys:
            if k == 'w':
                shape_index = move_index(shape_index + 1)
            elif k == 's':
                shape_index = move_index(shape_index - 1)
            elif k == 'd':
                shape_scale += 0.05
                change_size(shape_scale)
            elif k == 'a':
                shape_scale -= 0.05
                change_size(shape_scale)
    msg.text = f'Size: {shape_scale:0.2f}'
    dis_shape.draw()
    msg.draw()
    controls.draw()
    mywin.update()    