"""
Visual utility used to determine what size shapes should be and also
how far to the left and right stimuli should be displayed.
"""

from psychopy import visual, event # import some basic libraries from PsychoPy

from init import mywin, kb, InputTracker, scale, hor_scale, get_shape, shape_size

shape_scale = shape_size # Starting value

scale_unit = 0.05 # How much to increment or decrement

# Create a list of shape objects to cycle through
shapes = [get_shape(shape_str) for shape_str in
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
