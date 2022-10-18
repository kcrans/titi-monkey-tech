from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from psychopy.hardware import keyboard
from program_specs import *

mon = monitors.Monitor(monitor_name)
    #print(prefs.general['winType'])
    #print(mon.getSizePix())
    #[500, 500]
    #create a window

mywin = visual.Window(size=window_size, fullscr=True, color="black", monitor=mon, units="height")

    #print(mywin.useRetina)
    # With a retina screen, the vertical dimmensions are from -1 to 1
    # but with a normal display, they are from -0.5 to 0.5
    # (retina displays scale the normal paramters by 2)
    
hor_scale = window_size[0]/window_size[1]

if mywin.useRetina == False: # Not a retina screen
    scale = 0.5
else:
    scale = 1
print('Is using retina:', mywin.useRetina)    
def get_shape(shape_name):
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
            win=mywin, name='go_cross',
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
        strike_circle.contains = strike_mask.contains
        return strike_circle
    else:
        return None


# Initialize all the sound objects located in the folder 'assets'
trial_start_sound = Sound('assets/trialStartSoundStereo.wav', name='startsound', stereo = True)
click_sound = Sound('assets/clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('assets/negativeReinforcement.wav', name='negsound')
    
kb = keyboard.Keyboard() # Used for tracking escape key presses

# Create a mouse event class to track touch input
if touch_screen == False:
    touch_tracker = event.Mouse(visible=True, win=mywin)
        
    class input_tracker:
        def is_touched(self):
            return touch_tracker.getPressed()[0] == 1 # getTime?
        
else:
    touch_tracker = event.Mouse(visible=False, win=mywin)
    lastPos = touch_tracker.getPos()
    class input_tracker:
        def __init__(self):
            self.lastPos = touch_tracker.getPos()
        def is_touched(self):
            currentPos = touch_tracker.getPos()
            if currentPos[0] != self.lastPos[0] or currentPos[1] != self.lastPos[1]:
                self.lastPos = currentPos
                return True
            else:
                return False
