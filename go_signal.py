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

mon = monitors.Monitor('macbook')
print(prefs.general['winType'])
#[500, 500]
#create a window
mywin = visual.Window(size=[1440, 900], fullscr=False, color="black", monitor=mon, units="height")
#mywin.monitor.setCurrent('macbook.json')

#create a mouse event class to track touch input
touch_tracker = event.Mouse(visible=True, win=mywin)

trial_start_sound = Sound('assets/trialStartSoundStereo.wav', name='startsound', stereo = True)
click_sound = Sound('assets/clickSound.wav', name='clicksound')
neg_reinforce_sound = Sound('assets/negativeReinforcement.wav', name='negsound')


phases = {'Go Signal':0, 'Wait Screen':1, 'Alternating Stop Signal':2, 'Random Stop Signal':3, 'Experiment':4}

info = {'Subject ID':'charles', 'Subject Condition':'good', 'Phase': 'Alternating Stop Signal' }
info['dateStr'] = data.getDateStr()
infoDlg = gui.DlgFromDict(dictionary=info, title= 'test', fixed=['ExpVersion'])
if infoDlg.OK:
    print(info)
else:
    print('no')

fileName = info['Subject ID'] + info['dateStr']
dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
dataFile.write("subject id,subject condition,session timestamp,phase,trial number,stop stimulus,screen touched,response time,hold phase touches,direct touch,diameter\n")
def write_data(trial_num, stop_stim, screen_touched, response_time, direct_touch):
    dataFile.write(f"{info['Subject ID']},{info['Subject Condition']},{info['dateStr']},{phases[info['Phase']]},{trial_num},{stop_stim},{screen_touched},{response_time},0,{direct_touch},713\n")
    return

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
starttime = globalClock.getTime()
trialClock = core.Clock()
shapes = [circle, triangle] # 

i = 0

if info['Phase'] == 'Wait Screen':
    def new_shape(x):
        return 0
elif info['Phase'] == 'Alternating Stop Signal':
    def new_shape(x):
        return x % 2
        
elif info['Phase'] == 'Random Stop Signal':
    def new_shape(x): 
        return choice((0, 1))


while globalClock.getTime() < session_timeout_time - 6.0:
    index = new_shape(i)
    dis_shape = shapes[index]
    mywin.flip()
    side = choice((-1, 1))
    dis_shape.pos = (side*(0.4 - index*0.1), index*-.125)
    trial_start_sound.play()
    core.wait(hold_phase_delay)
    trialClock.reset()
    if index == 0:
        touched = False
        while trialClock.getTime() < 30.0 and globalClock.getTime() < session_timeout_time:
            event.clearEvents()
            dis_shape.draw()
            mywin.update()
            touch_tracker.clickReset() #Maybe run once outside the loop?

            if touch_tracker.getPressed(getTime=True)[0][0] == 1:
                touched = True
                if dis_shape.contains(touch_tracker) and index == 0:
                    write_data(i + 1, 'FALSE', 'TRUE', trialClock.getTime(), 'TRUE')
                    click_sound.play()
                    mywin.flip()
                    core.wait(positive_reinforcement_delay)
                else:
                    write_data(i + 1, 'FALSE', 'TRUE', trialClock.getTime(), 'FALSE')
                    neg_reinforce_sound.play()
                    mywin.flip()
                    core.wait(negative_reinforcement_delay)
                break # Break out of inner loop if anywhere on screen is touched
        if not touched:
            write_data(i + 1, 'FALSE', 'FALSE', trialClock.getTime(), 'FALSE')
    else:
        while globalClock.getTime() < session_timeout_time:
            if trialClock.getTime() >= 2.0:
                write_data(i + 1, 'TRUE', 'FALSE', trialClock.getTime(), 'FALSE')
                click_sound.play()
                mywin.flip()
                core.wait(positive_reinforcement_delay)
                break
            event.clearEvents()
            dis_shape.draw()
            mywin.update()
            touch_tracker.clickReset()
            if touch_tracker.getPressed(getTime=True)[0][0] == 1:
                write_data(i + 1, 'TRUE', 'TRUE', trialClock.getTime(), 'FALSE')
                neg_reinforce_sound.play()
                mywin.flip()
                core.wait(negative_reinforcement_delay)
                break # Break out of inner loop if anywhere on screen is touched
    i += 1
