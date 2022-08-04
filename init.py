from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from psychopy.hardware import keyboard
from parameters import *

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

if mywin.useRetina == False: # Not a retina screen
    scale = 0.5
else:
    scale = 1
    #print(mywin.size)


# Initialize all the sound objects located in the folder 'assets'
trial_start_sound = Sound('assets/trialStartSoundStereo.wav', name='startsound', stereo = True)
click_sound = Sound('assets/clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('assets/negativeReinforcement.wav', name='negsound')
    
kb = keyboard.Keyboard() # Used for tracking escape key presses

# Create a mouse event class to track touch input
if touch_screen == False:
        touch_tracker = event.Mouse(visible=True, win=mywin)
        def is_touched():
            return touch_tracker.getPressed()[0] == 1 # getTime?
        
else:
        touch_tracker = event.Mouse(visible=True, win=mywin)
        def is_touched():
            return touch_tracker.mouseMoved()

