"""
This module intitializes the visual environment, defines the various shapes,
loads the audio files, and sets up methods for touch input.
"""

from psychopy import visual, event, monitors
# ^ import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from psychopy.hardware import keyboard # for tracking keystokes

from program_specs import monitor_name, window_size, touch_screen, shape_size, font_size

mon = monitors.Monitor(monitor_name)

mywin = visual.Window(size=window_size, fullscr=True, color="black", monitor=mon, units="height")

# Find the ratio of screen width to height.
# This gives us our horizontal dimmensions

hor_scale = window_size[0]/window_size[1]

# With a retina screen, the vertical dimmensions are from -1 to 1
# but with a normal display, they are from -0.5 to 0.5
# (retina displays scale the normal paramters by 2)

if mywin.useRetina is True: # If it's a retina screen
    scale = 0.5
else:
    scale = 1

def get_shape(shape_name):
    """
    input: string with name of shape
    
    output: ShapeStim object or None if no shape corresponds to input string
    """
    # create circle stimuli
    if shape_name == 'circle':
        circle = visual.ShapeStim(
            win=mywin, name='go_circle',
            size=(shape_size, shape_size), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=4,     colorSpace='rgb', fillColor=None,
            lineColor = "White", opacity=None, interpolate=True)
        return circle

    # create triangle stimuli
    if shape_name == 'triangle':
        triangle = visual.ShapeStim(
            win=mywin, name='stop_triangle',
            size=(shape_size, shape_size), vertices='triangle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=4,     colorSpace='rgb', fillColor=None,
            lineColor = "Yellow", opacity=None, interpolate=True)
        return triangle

    # create square stimuli
    if shape_name == 'square':
        square = visual.rect.Rect(
            win=mywin, size = (shape_size - 0.1, shape_size - 0.1), pos=(0,0),
            fillColor=None, lineWidth=4, lineColor = "Red", name = "stop_square"
            )
        return square

    # create cross stimuli
    if shape_name == 'cross':
        cross_vertices = [
            (-0.12, +0.5),  # up
            (+0.12, +0.5),
            (+0.12, +0.12),
            (+0.5, +0.12),  # right
            (+0.5, -0.12),
            (+0.12, -0.12),
            (+0.12, -0.5),  # down
            (-0.12, -0.5),
            (-0.12, -0.12),
            (-0.5, -0.12),  # left
            (-0.5, +0.12),
            (-0.12, +0.12),
            ]
        cross = visual.ShapeStim(
            win=mywin, name='go_cross',
            size=(shape_size, shape_size), vertices=cross_vertices,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=4,     colorSpace='rgb', fillColor=None, lineColor = "Blue",
            opacity=None, interpolate=True)
        return cross

    # Create star stimuli
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
        star = visual.ShapeStim(
            win=mywin, name='go_cross',
            size=(shape_size + 0.1, shape_size + 0.1), vertices=star_points,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=4, lineColor = "Green", colorSpace='rgb', fillColor=None,
            opacity=None, interpolate=True)
        return star

    # create a circle with a cross in the center
    if shape_name == 'strike_circle':
        # Add an invisible circle in order to track touches
        strike_mask = visual.ShapeStim(
            win=mywin, name='go_circle',
            size=(shape_size, shape_size), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=1, opacity=0.0, interpolate=True)

        # Use an image instead of an animation
        strike_circle = visual.ImageStim(win=mywin,
        image='assets/goSignal_strike.png', size = (shape_size, shape_size))
        visible_draw = strike_circle.draw
        # Redefine the draw method to draw both visuals
        def new_draw():
            visible_draw()
            strike_mask.draw()
        strike_circle.draw = new_draw
        strike_circle.contains = strike_mask.contains
        return strike_circle
    # Else if input string doesn't match any of the cases
    return None


# Initialize all the sound objects located in the folder 'assets'
trial_start_sound = Sound('assets/trialStartSoundStereo.wav', name='startsound', stereo = True)
click_sound = Sound('assets/clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('assets/negativeReinforcement.wav', name='negsound')

kb = keyboard.Keyboard() # Used for tracking escape key presses

# Create a mouse event class to track touch input
if touch_screen is False: # When using regular mouse
    #touch_tracker = event.Mouse(visible=True, win=mywin)
    class InputTracker(event.Mouse):
        """ Tracks input with a mouse """
        def __init__(self):
            event.Mouse.__init__(self, visible = True, win = mywin)
        def is_touched(self):
            """ Is mouse right click currently pressed down? """
            return self.getPressed()[0] == 1

else: # When using a touch screen
    #touch_tracker = event.Mouse(visible=False, win=mywin)
    class InputTracker(event.Mouse):
        """ Tracks input with a touchscreen """
        def __init__(self):
            event.Mouse.__init__(self, visible=False, win=mywin)
            self.last_pos = self.getPos()
        def is_touched(self):
            """ Has the touchsreen mouse pointer moved? """
            current_pos = self.getPos()
            # If pointer moved at all:
            if current_pos[0] != self.last_pos[0] or current_pos[1] != self.last_pos[1]:
                self.last_pos = current_pos
                return True
            # Else if position of pointer hasn't changed:
            return False
            
            

shape_scale = shape_size # Starting value

scale_unit = 0.05 # How much to increment or decrement

# Create a list of shape objects to cycle through
shapes = [get_shape(shape_str) for shape_str in
['circle', 'triangle', 'square', 'cross', 'star']]
shape_index = 0 # Tracks which shape is displayed

def change_size(delta):
    for shape in shapes:
        old_size = shape.size[0]
        shape.size = (old_size + delta, old_size + delta)

hor_pos = 0.5*(hor_scale/2) # How far to go horizontally on the left and right
print(f'Scaling factor: {hor_scale} and horizontal position: {hor_pos}')

keys = kb.getKeys()
side = -1

size_msg = visual.TextStim(mywin, text=' ', pos=(0.0, 0.0),
color = (1.0, 0.0, 0.0), height= 0.05)
pos_msg = visual.TextStim(mywin, text=' ', pos=(hor_pos, 0.4),
color = (1.0, 0.0, 0.0), height= 0.05)
size_controls = visual.TextStim(mywin,
text='a, d: move left or right                   \n w, s: increase or decrease size ',
pos=(-1*hor_pos, -0.4), color = (1.0, 0.0, 0.0), height= 0.05)
pos_controls = visual.TextStim(mywin, text='space: flip side',
pos=(hor_pos, -0.4), color = (1.0, 0.0, 0.0), height= 0.05)
mywin.flip()
device = InputTracker()

hor_pos = 0
for dis_shape in shapes:
    dis_shape.pos = (0, 0)
    dis_shape.draw()
size_msg.text = f'Size: {shape_scale:0.2f}'
pos_msg.text = f'Position: {hor_pos:0.2f}'
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
            if k == 'w' and shape_scale <= 1.5:
                shape_scale += scale_unit
                change_size(scale_unit)
            elif k == 's' and shape_scale > scale_unit:
                shape_scale -= scale_unit
                change_size((-1)*scale_unit)
            elif k == "a":
                hor_pos -= scale_unit
            elif k == "d":
                hor_pos += scale_unit
            elif k == "space":
                hor_pos = -1*hor_pos
        for dis_shape in shapes:
            dis_shape.pos = (hor_pos, dis_shape.pos[1])
            dis_shape.draw()
        size_msg.text = f'Size: {shape_scale:0.2f}'
        pos_msg.text = f'Position: {hor_pos:0.2f}'
        size_msg.draw()
        pos_msg.draw()
        size_controls.draw()
        pos_controls.draw()
        mywin.flip()
mywin.close()
print(f'Shape scale: {shape_scale:0.4f}, Offset position: {hor_pos:0.4f}')

