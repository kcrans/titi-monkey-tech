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

def main():
    info = {'Subject ID':'TEST SUBJECT 1', 'Subject Condition':'unconditional', 'Phase': 'Alternating Stop Signal' }
    info['dateStr'] = data.getDateStr()
    infoDlg = gui.DlgFromDict(dictionary=info, title= 'Opening Menu', fixed=['ExpVersion'])
    #if infoDlg.OK:
    #    print(info)
    
    phases = {'Go Signal':0, 'Wait Screen':1, 'Alternating Stop Signal':2, 'Random Stop Signal':3, 'Experiment':4}



    fileName = info['Subject ID'] + info['dateStr']
    dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write("subject id,subject condition,session timestamp,phase,trial number,stop stimulus,screen touched,response time,hold phase touches,direct touch,diameter\n")
    def write_data(trial_num, stop_stim, screen_touched, response_time, direct_touch, hold_touches, diameter):
        dataFile.write(f"{info['Subject ID']},{info['Subject Condition']},{info['dateStr']},{phases[info['Phase']]},{trial_num},{stop_stim},{screen_touched},{response_time},{hold_touches},{direct_touch},{diameter}\n")
        return
    
    if True:
        from circle_training import circle_run
        circle_run(write_data)
'''    elif "Wait Screen":
        
    elif "Alternating Stop Signal":
        
    elif "Random Stop Signal":
        
    elif "Experiment":'''
        
    


if __name__ == "__main__":
    main()
