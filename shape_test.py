"""
Visual utility used to determine what size shapes should be and also
how far to the left and right stimuli should be displayed.
"""

from psychopy import visual, event # import some basic libraries from PsychoPy

from init import mywin, kb, InputTracker, scale, hor_scale

shape_scale = scale # Starting value

scale_unit = 0.05 # How much to increment or decrement

def get_shape(mywin, shape_name):
    """
    Input: Window object, name of shape (string)
    Output: Requested shape object
    """
    #create circle stimuli
    if shape_name == 'circle':
        circle = visual.BaseShapeStim(
            win=mywin, name='go_circle',
            size=(shape_scale, shape_scale), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=1,     colorSpace='rgb', fillColor='white',
            opacity=None, interpolate=True)
        return circle
    #create triangle stimuli
    if shape_name == 'triangle':
        triangle = visual.Polygon(
            win=mywin, edges=3, size=(shape_scale, shape_scale),
             pos=(0, -0.1),
            fillColor='grey', name='stop_triangle'
            )
        return triangle
    if shape_name == 'square':
        square = visual.rect.Rect(
            win=mywin, size = (shape_scale- 0.1, shape_scale - 0.1), pos=(0,0),
            fillColor='white', name = "stop_square"
            )
        return square
    if shape_name == 'cross':
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

        cross = visual.BaseShapeStim(
            win=mywin, name='go_cross',
            size=(shape_scale, shape_scale), vertices=cross_vertices,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=1,     colorSpace='rgb', fillColor='grey',
            opacity=None, interpolate=True)

        return cross
    if shape_name == 'star':
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
        star = visual.BaseShapeStim(
            win=mywin, name='star',
            size=(shape_scale, shape_scale), vertices=star_points,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=1,     colorSpace='rgb', fillColor='grey',
            opacity=None, interpolate=True)

        return star
    if shape_name == 'strike_circle':
        # Add an invisible circle in order to track touches
        strike_mask = visual.BaseShapeStim(
            win=mywin, name='go_circle',
            size=(shape_scale, shape_scale), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=1, opacity=0.0, interpolate=True)

        strike_circle = visual.ImageStim(win=mywin,
        image='assets/goSignal_strike.png', size = (shape_scale, shape_scale))
        visible_draw = strike_circle.draw
        def new_draw():
            visible_draw()
            strike_mask.draw()
        strike_circle.draw = new_draw
        return strike_circle
    # Else if string didn't correspond to a shape
    return None

# Create a list of shape objects to cycle through
shapes = [get_shape(mywin, shape_str) for shape_str in
['circle', 'triangle', 'square', 'cross', 'star', 'strike_circle' ]]
shape_index = 0 # Tracks which shape is displayed
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
print(f'Scaling factor: {hor_scale} and horizontal position: {hor_pos}')

keys = kb.getKeys()
side = -1

size_msg = visual.TextStim(mywin, text=' ', pos=(0.0, 0.0),
color = (1.0, 0.0, 0.0), height= 0.05)
pos_msg = visual.TextStim(mywin, text=' ', pos=(hor_pos, 0.4),
color = (1.0, 0.0, 0.0), height= 0.05)
size_controls = visual.TextStim(mywin,
text='w, s: cycle through shapes\na, d: change size                ',
pos=(-1*hor_pos, -0.4), color = (1.0, 0.0, 0.0), height= 0.05)
pos_controls = visual.TextStim(mywin, text='j, k: move left or right',
pos=(hor_pos, -0.4), color = (1.0, 0.0, 0.0), height= 0.05)
mywin.flip()
device = InputTracker()

hor_pos = 0
dis_shape = shapes[shape_index]
dis_shape.pos = (0, 0)
size_msg.text = f'Size: {shape_scale:0.2f}'
pos_msg.text = f'Position: {hor_pos:0.2f}'
dis_shape.draw()
size_msg.draw()
pos_msg.draw()
size_controls.draw()
pos_controls.draw()
mywin.flip()
while 'escape' not in keys:
    event.clearEvents()
    keys = kb.getKeys()
    if keys:
        for k in keys:
            if k == 'w':
                shape_index = move_index(shape_index + 1)
            elif k == 's':
                shape_index = move_index(shape_index - 1)
            elif k == 'd' and shape_scale <= 1.5:
                shape_scale += scale_unit
                change_size(shape_scale)
            elif k == 'a' and shape_scale > scale_unit:
                shape_scale -= scale_unit
                change_size(shape_scale)
            elif k == "j":
                hor_pos -= scale_unit
            elif k == "k":
                hor_pos += scale_unit
        dis_shape = shapes[shape_index]
        dis_shape.pos = (hor_pos, 0)
        size_msg.text = f'Size: {shape_scale:0.2f}'
        pos_msg.text = f'Position: {hor_pos:0.2f}'
        dis_shape.draw()
        size_msg.draw()
        pos_msg.draw()
        size_controls.draw()
        pos_controls.draw()
        mywin.flip()
mywin.close()
print(f'Shape scale: {shape_scale:0.4f}, Offset position: {hor_pos:0.4f}')
