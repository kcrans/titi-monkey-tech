#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function used to run any of the trainings/experiments
"""

__author__ = "Kaleb Crans"
__version__ = "0.99"
__license__ = "MIT"

import os
import json
import csv
from random import choice # for randomness in the display of stimuli

# import some basic libraries from PsychoPy
# gui for selecting subject and experiment
# data for getting the date/time
from psychopy import gui, data

# Get parameters for gui interface
from program_specs import touch_screen, font_size

def main(debug = False):
    """
    Presents gui options for different experiments, runs experiments, and
    the records results in titi_monkey_data.csv. Set debug flag to True to
    print out helpful messages
    """
    phase_names = ['0: Go Signal', '1: Wait Screen',
    '2: Alternating Stop Signal', '3: Random Stop Signal', '4: Experiment' ]
    # Load all the metadata about prior subject
    with open('subinfo.json', 'r', encoding = 'utf-8') as param_file:
        subjects = json.load(param_file)
    sub_dlg = gui.Dlg(title= f'TITI Beta Version {__version__}')
    
    if touch_screen: # Increase size of font/buttons to make input easier
        # Create a new, custom stylesheet
        style_sheet = """
QWidget      {
        font-size: 30px;
        }
QComboBox {
    border: 1px solid gray;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
    font-size: 30px;
}

QComboBox:editable {
    background: white;
}

QComboBox:!editable, QComboBox::drop-down:editable {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

/* Background color of popup-list.*/ 
QComboBox QListView{
    background-color:white;
    border:1px solid gray;
}
/* Needed to complete the rule set. */
QComboBox::item:alternate {
    background: white;
}
/* Color of the selected list item. */
QComboBox::item:selected {
    border: 1px solid transparent;
    background:yellow;
}

QComboBox::indicator{
    background-color:transparent;
    selection-background-color:transparent;
    color:transparent;
    selection-color:transparent;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
    image: url(1downarrow.png);
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
    }
QLineEdit {
    border: 2px solid gray;
    border-radius: 10px;
    padding: 0 8px;
    background: yellow;
    selection-background-color: darkgray;
}
        """
        sub_dlg.setStyleSheet(style_sheet)

    sub_dlg.addText('Subject Info')
    sub_dlg.addField("Name:", choices = list(subjects.keys()))
    subject_choice = sub_dlg.show()
    if sub_dlg.OK:
        subject_choice = subject_choice[0]
        if debug:
            print('Subject chosen')
    else:
        return # End early

    current_sub = subjects[subject_choice] # Object containing info about selection
    phase_names.insert(0, phase_names.pop(int(current_sub['current phase'])))

    confir_dlg = gui.Dlg(title= f'TITI Beta Version {__version__}')
    
    if touch_screen:
        print("changed")
        # Change style for the second dialog also
        confir_dlg.setStyleSheet(style_sheet)
    
    confir_dlg.addText(f'Info for subject {subject_choice}')
    confir_dlg.addField("Condition:", current_sub['condition'])
    confir_dlg.addField("Phase:", choices = phase_names)
    confir_dlg.addField("Session time:", current_sub['session timeout time'])

    pos_shape_name = current_sub['positive stimuli']
    neg_shape_name = current_sub['negative stimuli']

    phase_choice = confir_dlg.show()
    if confir_dlg.OK:
        sub_cond, chosen_phase, session_timeout_time = phase_choice
        if debug:
            print('Selection made, starting now')
    else:
        return # End before it starts

    session_timeout_time = float(session_timeout_time)
    common_params = current_sub["phase 1-3 params"]
    param_list = [
    common_params["pos_duration"],
    common_params["neg_duration"],
    common_params["negative_reinforcement_delay"],
    common_params["positive_reinforcement_delay"],
    common_params["hold_phase_delay"]
    ]

    timestamp = data.getDateStr()

    file_name = "titi_monkey_data.csv"
    # If the csv file doesn't exist, create it and add the column headings:
    if not os.path.exists(file_name):
        with open(file_name, 'w+', newline = ' ', encoding = 'utf-8') as data_file:
            csv_writer = csv.writer(data_file, delimiter=',')
            csv_writer.writerow([
            "subject id", "subject condition", "session timestamp",
            "phase", "trial number", "stop stimulus", "screen touched",
            "response time", "hold phase touches", "direct touch",
            "diameter", "session time", "positive shape", "negative shape",
            "go stim duration", "stop stim duration",
            "negative reinforcement delay", "positive reinforcement delay",
            "hold phase delay"])

    with open(file_name, 'a', newline = '', encoding = 'utf-8') as data_file:
        csv_writer = csv.writer(data_file, delimiter=',')
        def write_data(trial_num, stop_stim, screen_touched, response_time,
        hold_touches, direct_touch, scale):
            csv_writer.writerow([
            subject_choice, sub_cond, timestamp, chosen_phase, trial_num,
            stop_stim, screen_touched, response_time, hold_touches,
            direct_touch, scale, session_timeout_time, pos_shape_name,
            neg_shape_name, *param_list])

        if chosen_phase == '0: Go Signal':
            from circle_training import circle_run
            completed = circle_run(debug, write_data, session_timeout_time,
            current_sub["phase 0 params"])

        elif chosen_phase == "1: Wait Screen":
            from varied_training import normal_training
            def new_shape(trial_num):
                """
                Ignore input
                Always return index 0, which will be the positive stimuli
                """
                return 0
            completed = normal_training(debug, write_data, new_shape,
            session_timeout_time, pos_shape_name, neg_shape_name, common_params)

        elif chosen_phase == "2: Alternating Stop Signal":
            from varied_training import normal_training
            def new_shape(trial_num):
                """
                Take modulus of input
                Alternate between positive and negative (indices 0 and 1) stimuli
                """
                return trial_num % 2
            completed = normal_training(debug, write_data, new_shape,
            session_timeout_time, pos_shape_name, neg_shape_name, common_params)

        elif chosen_phase == "3: Random Stop Signal":
            from varied_training import normal_training
            def new_shape(trial_num):
                """
                Ignore input
                Choose a positive or negative stimulus randomly
                """
                return choice((0, 1))
            completed = normal_training(debug, write_data, new_shape, 
            session_timeout_time, pos_shape_name, neg_shape_name, common_params)

        elif chosen_phase == "4: Experiment":
            from experiment import run_experiment
            completed = run_experiment(debug, write_data, pos_shape_name,
            neg_shape_name, common_params, current_sub["phase 4 params"])
    if debug:
        print(f'Experiment completed: {completed}')
    # Record any changes to subject parameters
    current_sub['condition'] = sub_cond
    current_sub['current phase'] = int(chosen_phase[0])
    current_sub['session timeout time'] = session_timeout_time
    with open('subinfo.json', "w", encoding = 'utf-8') as param_file:
        json.dump(subjects, param_file)
if __name__ == "__main__":
    main(True)
