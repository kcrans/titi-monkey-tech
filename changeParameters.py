from psychopy import gui
import json

def new_dictionary(list_values):
    new_dict = {}
    new_dict["condition"] = next(list_values)
    new_dict["current phase"] = next(list_values)
    new_dict["session timeout time"] = next(list_values)
    new_dict_a = {}
    new_dict_a["touch_delay"] = next(list_values)
    new_dict_a["start"] = next(list_values)
    new_dict_a["upper_bound"] = next(list_values)
    new_dict_a["lower_bound"] = next(list_values)
    new_dict_a["increment"] = next(list_values)
    new_dict["phase 0 params"] = new_dict_a
    new_dict_b = {}
    new_dict_b["negative_reinforcement_delay"] = next(list_values)
    new_dict_b["positive_reinforcement_delay"] = next(list_values)
    new_dict_b["hold_phase_delay"] = next(list_values)
    new_dict_b["circle_diam"] = next(list_values)
    new_dict_b["pos_duration"] = next(list_values)
    new_dict_b["neg_duration"] = next(list_values)
    new_dict["phase 1-3 params"] = new_dict_b
    new_dict_c = {}
    new_dict_c["num_pos"] = next(list_values)
    new_dict_c["num_neg"] = next(list_values)
    new_dict["phase 4 params"] = new_dict_c
    return new_dict



phase_names = ['0: Go Signal', '1: Wait Screen', '2: Alternating Stop Signal', '3: Random Stop Signal', '4: Experiment' ]
# Load all the metadata about prior subjects
with open('subinfo.json') as f:
    subjects = json.load(f)
subStrings = list(subjects.keys())
subStrings.append("NEW Subject")
subDlg = gui.Dlg(title= f'TITI')
subDlg.addText('Subject Info')
subDlg.addField("Name:", choices = subStrings)
subject_choice = subDlg.show()[0]
if subDlg.OK:
    print('Subject chosen')
    if subject_choice == "NEW Subject":
        parDlg = gui.Dlg(title= 'Add New Subject')
        parDlg.addField("Name", "", color="Blue")
        parDlg.addText("Global Parameters", color="Blue")
        parDlg.addField("Condition:", "paired")
        parDlg.addField("Current phase:", "2")
        parDlg.addField("Session timeout time:", "30")
        parDlg.addText("Parameters for phase 0:", color="Blue")
        parDlg.addField("Touch delay:", "0.25")
        parDlg.addField("Start:", "0.8")
        parDlg.addField("Upper bound:", "0.9")
        parDlg.addField("Lower bound:", "0")
        parDlg.addField("Increment:", "0.05")
        parDlg.addText("Parameters for phases 1-3:", color="Blue")
        parDlg.addField("Negative reinforcement delay:", "3.0")
        parDlg.addField("Positive reinforcement delay:", "1.0")
        parDlg.addField("Hold phase delay:", "2")
        parDlg.addField("Circle diameter:", "0.8")
        parDlg.addField("Positive stimuli duration:", "30")
        parDlg.addField("Negative stimuli duration:", "2.0")
        parDlg.addText("Parameters for phase 4, in addition to above:", color="Blue")    
        parDlg.addField("Number of positive stimuli:", "2")
        parDlg.addField("Number of negative stimuli:", "4")
        values = parDlg.show()
        values_iterator = iter(values)
        sub_name = next(values_iterator)
        subjects[sub_name] = new_dictionary(values_iterator)
        
    else:
        current_sub = subjects[subject_choice] # Object containing info about selection
        parDlg = gui.Dlg(title= f'TITI')
        parDlg.addText("Global Parameters", color="Blue")
        parDlg.addField("Condition:", current_sub["condition"])
        parDlg.addField("Current phase:", current_sub["current phase"])
        parDlg.addField("Session timeout time:", current_sub["session timeout time"])
        parDlg.addText("Parameters for phase 0:", color="Blue")
        current_phase_a = current_sub["phase 0 params"]
        parDlg.addField("Touch delay:", current_phase_a["touch_delay"])
        parDlg.addField("Start:", current_phase_a["start"])
        parDlg.addField("Upper bound:", current_phase_a["upper_bound"])
        parDlg.addField("Lower bound:", current_phase_a["lower_bound"])
        parDlg.addField("Increment:", current_phase_a["increment"])
        parDlg.addText("Parameters for phases 1-3:", color="Blue")
        current_phase_b = current_sub["phase 1-3 params"]
        parDlg.addField("Negative reinforcement delay:", current_phase_b["negative_reinforcement_delay"])
        parDlg.addField("Positive reinforcement delay:", current_phase_b["positive_reinforcement_delay"])
        parDlg.addField("Hold phase delay:", current_phase_b["hold_phase_delay"])
        parDlg.addField("Circle diameter:", current_phase_b["circle_diam"])
        parDlg.addField("Positive stimuli duration:", current_phase_b["pos_duration"])
        parDlg.addField("Negative stimuli duration:", current_phase_b["neg_duration"])
        parDlg.addText("Parameters for phase 4, in addition to above:", color="Blue")    
        current_phase_c = current_sub["phase 4 params"]
        parDlg.addField("Number of positive stimuli:", current_phase_c["num_pos"])
        parDlg.addField("Number of negative stimuli:", current_phase_c["num_neg"])
        values = parDlg.show()
        values_iterator = iter(values)
        subjects[subject_choice] = new_dictionary(values_iterator)
with open('subinfo.json', "w") as f:
    json.dump(subjects, f)

