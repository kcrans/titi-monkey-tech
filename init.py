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
            lineWidth=0.0,     colorSpace='rgb', fillColor='white',
            opacity=None, interpolate=True)
        return circle

    # create triangle stimuli
    if shape_name == 'triangle':
        triangle = visual.Polygon(
            win=mywin, edges=3, size=(shape_size, shape_size),
             pos=(0, -0.1),
            fillColor='grey', name='stop_triangle'
            )
        return triangle

    # create square stimuli
    if shape_name == 'square':
        square = visual.rect.Rect(
            win=mywin, size = (shape_size- 0.1, shape_size - 0.1), pos=(0,0),
            fillColor='white', name = "stop_square"
            )
        return square

    # create cross stimuli
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
        cross = visual.ShapeStim(
            win=mywin, name='go_cross',
            size=(shape_size, shape_size), vertices=cross_vertices,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0,     colorSpace='rgb', fillColor='grey',
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
            size=(shape_size, shape_size), vertices=star_points,
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0,     colorSpace='rgb', fillColor='grey',
            opacity=None, interpolate=True)
        return star

    # create a circle with a cross in the center
    if shape_name == 'strike_circle':
        # Add an invisible circle in order to track touches
        strike_mask = visual.ShapeStim(
            win=mywin, name='go_circle',
            size=(shape_size, shape_size), vertices='circle',
            ori=0.0, pos=(0, 0), anchor='center',
            lineWidth=0.0, opacity=0.0, interpolate=True)

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
    class InputTracker:
        """ Tracks input with a mouse """
        def __init__(self):
            self.tracker = event.Mouse(visible=True, win=mywin)
        def is_touched(self):
            """ Is mouse right click currently pressed down? """
            return self.tracker.getPressed()[0] == 1
        def get_pos(self):
            return self.tracker.getPos()

else: # When using a touch screen
    #touch_tracker = event.Mouse(visible=False, win=mywin)
    class InputTracker:
        """ Tracks input with a touchscreen """
        def __init__(self):
            self.tracker = event.Mouse(visible=False, win=mywin)
            self.last_pos = self.tracker.getPos()
        def is_touched(self):
            """ Has the touchsreen mouse pointer moved? """
            current_pos = self.tracker.getPos()
            # If pointer moved at all:
            if current_pos[0] != self.last_pos[0] or current_pos[1] != self.last_pos[1]:
                self.last_pos = current_pos
                return True
            # Else if position of pointer hasn't changed:
            return False
