#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main fucntion used to run any of the trainings/experiments
"""

__author__ = "Kaleb Crans"
__version__ = "0.9"
__license__ = "MIT"

from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np
import json

def main():
    phase_names = ['Go Signal', 'Wait Screen', 'Alternating Stop Signal', 'Random Stop Signal', 'Experiment' ]
    with open('subinfo.json') as f:
        subjects = json.load(f)
    info = {'Subject ID':subjects['strings'], 'Subject Condition':'unconditional', 'Phase': phase_names }
    info['dateStr'] = data.getDateStr()
    infoDlg = gui.DlgFromDict(dictionary=info, title= f'TITI Beta Version {__version__}', fixed=['ExpVersion'])
    if infoDlg.OK:
        print('gui working')
    else:
        return # End program then and there
    
    phases = {'Go Signal':0, 'Wait Screen':1, 'Alternating Stop Signal':2, 'Random Stop Signal':3, 'Experiment':4}

    fileName = f"{info['Subject ID']}_{info['dateStr']}"
    dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write("subject id,subject condition,session timestamp,phase,trial number,stop stimulus,screen touched,response time,hold phase touches,direct touch,diameter\n")
    def write_data(trial_num, stop_stim, screen_touched, response_time, direct_touch, hold_touches, diameter):
        dataFile.write(f"{info['Subject ID']},{info['Subject Condition']},{info['dateStr']},{phases[info['Phase']]},{trial_num},{stop_stim},{screen_touched},{response_time},{hold_touches},{direct_touch},{diameter}\n")
        return
    
    chosen_phase =  info['Phase']
    
    if chosen_phase == 'Go Signal':
        from circle_training import circle_run
        circle_run(write_data)
        
    elif chosen_phase == "Wait Screen":
        from go_signal import normal_training
        def new_shape(x):
            return 0
        normal_training(write_data, new_shape)
    elif chosen_phase == "Alternating Stop Signal":
        from go_signal import normal_training
        def new_shape(x):
            return x % 2
        normal_training(write_data, new_shape)
    elif chosen_phase == "Random Stop Signal":
        from go_signal import normal_training
        def new_shape(x): 
            return choice((0, 1))
        normal_training(write_data, new_shape)
    elif chosen_phase == "Experiment":
        from experiment import run_experiment
        run_experiment(write_data)
    
if __name__ == "__main__":
    main()
