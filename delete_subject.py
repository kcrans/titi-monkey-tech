""" Module to remove a subject and associated parameters """
import json

from psychopy import gui

# Load all the metadata about subjects
with open('subinfo.json', 'r', encoding = 'utf-8') as f:
    subjects = json.load(f)

# Get an unsorted list of all subject names
subStrings = list(subjects.keys())

subDlg = gui.Dlg(title= "Choose subject to remove")
subDlg.addField("Subject Name:", choices = subStrings)

sub_results = subDlg.show()

if subDlg.OK:
    print("Subject chosen")
    confirmDlg = gui.Dlg(title= "Confirmation")
    confirmDlg.addText("Are you sure?")
    gui_results = confirmDlg.show()
    if confirmDlg.OK:
        sub_name = sub_results[0]
        print(f'{sub_name} removed')
        del subjects[sub_name]
    else:
        print("Whew, almost gone forever")
else:
    print("Exited early")

# Store the (potentially) updated json data
with open('subinfo.json', "w", encoding = 'utf-8') as f:
    json.dump(subjects, f)
