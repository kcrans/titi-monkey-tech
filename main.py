#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function used to run any of the trainings/experiments
"""

__author__ = "Kaleb Crans"
__version__ = "0.95"
__license__ = "MIT"

from psychopy import visual, core, event, monitors, prefs, gui, data  # import some basic libraries from PsychoPy
from psychopy.sound import Sound # methods for handling audio
from random import choice # for randomness in the display of stimuli
import numpy as np
import json
import os
import csv

def main():
    phase_names = ['0: Go Signal', '1: Wait Screen', '2: Alternating Stop Signal', '3: Random Stop Signal', '4: Experiment' ]
    # Load all the metadata about prior subject
    with open('subinfo.json') as f:
        subjects = json.load(f)
    subDlg = gui.Dlg(title= f'TITI Beta Version {__version__}')
    subDlg.addText('Subject Info')
    subDlg.addField("Name:", choices = list(subjects.keys()))
    subject_choice = subDlg.show()
    if subDlg.OK:
        subject_choice = subject_choice[0]
        print('Subject chosen')
    else:
        return # End early
    
    current_sub = subjects[subject_choice] # Object containing info about selection
    phase_names.insert(0, phase_names.pop(int(current_sub['current phase'])))
    
    confirDlg = gui.Dlg(title= f'TITI Beta Version {__version__}')
    confirDlg.addText(f'Info for subject {subject_choice}')
    confirDlg.addField("Condition:", current_sub['condition'])
    confirDlg.addField("Phase:", choices = phase_names)
    confirDlg.addField("Session time:", current_sub['session timeout time'])
    
    pos_shape_name = current_sub['positive stimuli']
    neg_shape_name = current_sub['negative stimuli']
    
    sub_cond, chosen_phase, session_timeout_time = confirDlg.show()
    session_timeout_time = float(session_timeout_time)
    common_params = current_sub["phase 1-3 params"]
    #param_string = f'{common_params["pos_duration"]},{common_params["neg_duration"]},{common_params["negative_reinforcement_delay"]},{common_params["positive_reinforcement_delay"]},{common_params["hold_phase_delay"]}'
    param_list = [common_params["pos_duration"], common_params["neg_duration"], common_params["negative_reinforcement_delay"], common_params["positive_reinforcement_delay"], common_params["hold_phase_delay"]]
    
    if confirDlg.OK:
        print('Selection made, starting now')
    else:
        return # End before it starts
    timestamp = data.getDateStr()
    
    fileName = f"titi_monkey_data.csv"
    # a simple text file with 'comma-separated-values'
    if not os.path.exists(fileName):
        with open(fileName, 'w+', newline='') as dataFile:
            csv_writer = csv.writer(dataFile, delimiter=',')
            csv_writer.writerow(["subject id", "subject condition", "session timestamp", "phase",
            "trial number", "stop stimulus", "screen touched", "response time",
            "hold phase touches", "direct touch", "diameter", "session time",
            "positive shape", "negative shape", "go stim duration", "stop stim duration",
            "negative reinforcement delay", "positive reinforcement delay", "hold phase delay"])
           # heading = "subject id,subject condition,session timestamp,phase,"
           # heading += "trial number,stop stimulus,screen touched,response time,"
            #heading += "hold phase touches,direct touch,diameter,session time,"
            #heading += "positive shape, negative shape,"
           # heading += "go stim duration,stop stim duration,negative reinforcement delay"
            #heading += ",positive reinforcement delay,hold phase delay\n"
           # dataFile.write(heading)
        
    with open(fileName, 'a', newline='') as dataFile:
        csv_writer = csv.writer(dataFile, delimiter=',')
        def write_data(trial_num, stop_stim, screen_touched, response_time, hold_touches, direct_touch, scale):
            csv_writer.writerow([subject_choice, sub_cond, timestamp, chosen_phase, trial_num, stop_stim, screen_touched, response_time, hold_touches, direct_touch, scale, session_timeout_time, pos_shape_name, neg_shape_name, *param_list])
            #return f"{subject_choice},{sub_cond},{timestamp},{chosen_phase},{trial_num},{stop_stim},{screen_touched},{response_time},{hold_touches},{direct_touch},{scale},{session_timeout_time},{pos_shape_name},{neg_shape_name},{param_string}\n"
            
        if chosen_phase == '0: Go Signal':
            from circle_training import circle_run
            for trial in circle_run(write_data, session_timeout_time, current_sub["phase 0 params"]):
                write_data(*trial)
        elif chosen_phase == "1: Wait Screen":
            from varied_training import normal_training
            def new_shape(x):
                return 0
            for trial in normal_training(write_data, new_shape, session_timeout_time, pos_shape_name, neg_shape_name, common_params):
                write_data(*trial)
        elif chosen_phase == "2: Alternating Stop Signal":
            from varied_training import normal_training
            def new_shape(x):
                return x % 2
            for trial in normal_training(write_data, new_shape, session_timeout_time, pos_shape_name, neg_shape_name, common_params):
                write_data(*trial)
        elif chosen_phase == "3: Random Stop Signal":
            from varied_training import normal_training
            def new_shape(x): 
                return choice((0, 1))
            for trial in normal_training(write_data, new_shape, session_timeout_time, pos_shape_name, neg_shape_name, common_params):
                write_data(*trial)
        elif chosen_phase == "4: Experiment":
            from experiment import run_experiment
            run_experiment(write_data, pos_shape_name, neg_shape_name, common_params, current_sub["phase 4 params"])
    
    # Record any changes to subject parameters
    current_sub['condition'] = sub_cond
    current_sub['current phase'] = int(chosen_phase[0])
    current_sub['session timeout time'] = session_timeout_time
    with open('subinfo.json', "w") as f:
        json.dump(subjects, f)
if __name__ == "__main__":
    main()
