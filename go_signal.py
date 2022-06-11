#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np

# Parameters
negative_reinforcement_delay = 3.0
positive_reinforcement_delay = 1.0
hold_phase_delay = 0.5 
session_timeout_time = 30 # Normallly 480.0 seconds

mon = monitors.Monitor('kalebs_desktop')
print(prefs.general['winType'])
#[500, 500]
#create a window
mywin = visual.Window(size=[2048, 1152], fullscr=False, color="black", monitor=mon, units="height")
#mywin.monitor.setCurrent('macbook.json')

#create a mouse event class to track touch input
touch_tracker = event.Mouse(visible=True, win=mywin)

trial_start_sound = Sound('trialStartSoundStereo.wav', name='startsound', stereo = True)
click_sound = Sound('clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('negativeReinforcement.wav', name='negsound')


info = {'name':'charles', 'ExpVersion':1.1 }
info['dateStr'] = data.getDateStr()
infoDlg = gui.DlgFromDict(dictionary=info, title= 'test', fixed=['ExpVersion'])
if infoDlg.OK:
    print(info)
else:
    print('no')

fileName = info['name'] + info['dateStr']
dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
dataFile.write('name,time,success\n')


#create circle stimuli
circle = visual.ShapeStim(
    win=mywin, name='go_circle',
    size=(0.8, 0.8), vertices='circle',
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=0.0,     colorSpace='rgb', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)
    
#create triangle stimuli
    
triangle = visual.Polygon(
    win=mywin, edges=3, size=(1, 1),
    anchor='center', pos=(0.3, 0),
    fillColor='grey', name='stop_triangle'
    )
print(circle.units)
#circle2 = visual.Circle(win = mywin, name='g', size)
#draw the stimuli and update the window

globalClock = core.Clock()
trialClock = core.Clock()
shapes = [circle, triangle] # 

i = 0

added = np.array([[0.4, 0] for i in range(100)])
right = circle.vertices + added
left = circle.vertices - added

print(np.shape(added))
while globalClock.getTime() < session_timeout_time - 6.0:
    index = i % 2
    dis_shape = shapes[index]
    mywin.flip()
    side = choice((-1, 1))
    dis_shape.pos = (side*(0.4 - index*0.1), index*-.125)
    #if index == 0:
     #   if side == -1:
     #       dis_shape.vertices = left
     #   else:
      #      dis_shape.vertices = right
    trial_start_sound.play()
    core.wait(hold_phase_delay)
    trialClock.reset()
    while trialClock.getTime() < 30.0 and globalClock.getTime() < session_timeout_time:
        event.clearEvents()
        dis_shape.draw()
        mywin.update()
        touch_tracker.clickReset()

        if touch_tracker.getPressed(getTime=True)[0][0] == 1:
            if dis_shape.contains(touch_tracker) and index == 0:
                dataFile.write(f'{info["name"]},{trialClock.getTime()},type,yes\n')
                click_sound.play()
                mywin.flip()
                core.wait(positive_reinforcement_delay)
            else:
                dataFile.write(f'{info["name"]},{trialClock.getTime()},type,no\n')
                neg_reinforce_sound.play()
                mywin.flip()
                core.wait(negative_reinforcement_delay)
            break # Break out of inner loop if anywhere on screen is touched
    i += 1

    
    
    #buttons, times = touch_tracker.
#pause, so you get a chance to see it!
#core.wait(5.0)
