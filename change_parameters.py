'''
Graphical program used to modify the JSON configuration file.
'''
import json

from psychopy import gui

# Get parameters for gui interface
from program_specs import touch_screen, font_size

def bring_to_front(shapes, last_selection):
    """
    Used to put the current selection at the front of the list.
    This makes it the default in the dropdown menu.
    """
    new_shapes = [shape for shape in shapes if shape != last_selection]
    new_shapes.insert(0, last_selection)
    return new_shapes
def new_dictionary(list_values):
    """
    Takes in a list of parameters and converts it into the correct
    dictionary used for JSON storage.
    """
    new_dict = {}
    new_dict["condition"] = next(list_values)
    new_dict["current phase"] = int(next(list_values)[0])
    new_dict["session timeout time"] = next(list_values)
    new_dict["positive stimuli"] = next(list_values)
    new_dict["negative stimuli"] = next(list_values)
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
    new_dict_b["shape_size"] = next(list_values)
    new_dict_b["pos_duration"] = next(list_values)
    new_dict_b["neg_duration"] = next(list_values)
    new_dict["phase 1-3 params"] = new_dict_b
    new_dict_c = {}
    new_dict_c["num_pos"] = next(list_values)
    new_dict_c["num_neg"] = next(list_values)
    new_dict["phase 4 params"] = new_dict_c
    return new_dict

# Default lists
phase_names = ['0: Go Signal', '1: Wait Screen', '2: Alternating Stop Signal'
, '3: Random Stop Signal', '4: Experiment' ]
shape_names = ['circle', 'triangle', 'square', 'cross', 'star', 'strike_circle']

# Load all the metadata about prior subjects
with open('subinfo.json', 'r', encoding = 'utf-8') as f:
    subjects = json.load(f)

# Get all the subject names
subStrings = list(subjects.keys())
# Add an option for new subject
subStrings.append("NEW Subject")


subDlg = gui.Dlg(title= "Choose or add subject")
og_font = subDlg.font()
og_font.setPointSize(30)
#print(gui.QtWidgets.QStyleFactory)
#print((subDlg.font()).pointSize())

font = gui.QtGui.QFont()
font.setFamily("Arial")
font.setPointSize(30)
subDlg.setFont(og_font)
print(subDlg.fontInfo().pointSize())

subDlg.addText('Subject Info')
subDlg.addField("Name:", choices = subStrings)

gui_results = subDlg.show()

if subDlg.OK:
    subject_choice = gui_results[0]
    print('Subject chosen')
    if subject_choice == "NEW Subject":
        parDlg = gui.Dlg(title= 'Add New Subject')
        parDlg.addField("Name", "", color="Blue")
        parDlg.addText("Global Parameters", color="Blue")
        parDlg.addField("Condition:", "paired")
        parDlg.addField("Current phase:", choices = phase_names)
        parDlg.addField("Session timeout time:", 30)
        parDlg.addField("Positive stimuli:", choices = shape_names)
        parDlg.addField("Negative stimuli:", choices = bring_to_front(shape_names, "triangle"))
        parDlg.addText("Parameters for phase 0:", color="Blue")
        parDlg.addField("Touch delay:", 0.25)
        parDlg.addField("Start:", 0.8)
        parDlg.addField("Upper bound:", 0.9)
        parDlg.addField("Lower bound:", 0)
        parDlg.addField("Increment:", 0.05)
        parDlg.addText("Parameters for phases 1-3:", color="Blue")
        parDlg.addField("Negative reinforcement delay:", 3.0)
        parDlg.addField("Positive reinforcement delay:", 1.0)
        parDlg.addField("Hold phase delay:", 2)
        parDlg.addField("Shape size:", 0.6)
        parDlg.addField("Positive stimuli duration:", 30)
        parDlg.addField("Negative stimuli duration:", 2.0)
        parDlg.addText("Parameters for phase 4,  in addition to above:", color="Blue")
        parDlg.addField("Number of positive stimuli:", 2)
        parDlg.addField("Number of negative stimuli:", 4)
        values = parDlg.show()
        if parDlg.OK:
            values_iterator = iter(values)
            sub_name = next(values_iterator)
            subjects[sub_name] = new_dictionary(values_iterator)
            print('Added new subject')
        else:
            print('Exited early')
    else:
        current_sub = subjects[subject_choice] # Object containing info about selection
        parDlg = gui.Dlg(title= f"Modify {subject_choice}'s parameters")
        parDlg.addText("Global Parameters", color="Blue")
        parDlg.addField("Condition:", current_sub["condition"])
        parDlg.addField("Current phase:",
        choices = bring_to_front(phase_names, phase_names[current_sub["current phase"]]))
        parDlg.addField("Session timeout time:", current_sub["session timeout time"])
        parDlg.addField("Positive stimuli:",
        choices = bring_to_front(shape_names, current_sub["positive stimuli"]))
        parDlg.addField("Negative stimuli:",
        choices = bring_to_front(shape_names, current_sub["negative stimuli"]))
        parDlg.addText("Parameters for phase 0:", color="Blue")
        current_phase_a = current_sub["phase 0 params"]
        parDlg.addField("Touch delay:", current_phase_a["touch_delay"])
        parDlg.addField("Start:", current_phase_a["start"])
        parDlg.addField("Upper bound:", current_phase_a["upper_bound"])
        parDlg.addField("Lower bound:", current_phase_a["lower_bound"])
        parDlg.addField("Increment:", current_phase_a["increment"])
        parDlg.addText("Parameters for phases 1-3:", color="Blue")
        current_phase_b = current_sub["phase 1-3 params"]
        parDlg.addField("Negative reinforcement delay:",
        current_phase_b["negative_reinforcement_delay"])
        parDlg.addField("Positive reinforcement delay:",
        current_phase_b["positive_reinforcement_delay"])
        parDlg.addField("Hold phase delay:", current_phase_b["hold_phase_delay"])
        parDlg.addField("Shape size:", current_phase_b["shape_size"])
        parDlg.addField("Positive stimuli duration:", current_phase_b["pos_duration"])
        parDlg.addField("Negative stimuli duration:", current_phase_b["neg_duration"])
        parDlg.addText("Parameters for phase 4,  in addition to above:", color="Blue")
        current_phase_c = current_sub["phase 4 params"]
        parDlg.addField("Number of positive stimuli:", current_phase_c["num_pos"])
        parDlg.addField("Number of negative stimuli:", current_phase_c["num_neg"])
        values = parDlg.show()
        if parDlg.OK:
            values_iterator = iter(values)
            subjects[subject_choice] = new_dictionary(values_iterator)
            print(f"Modified {subject_choice}'s info")
        else:
            print('Exited early')
else:
    print('Exited early')

with open('subinfo.json', "w", encoding = 'utf-8') as f:
    json.dump(subjects, f)
