from psychopy import gui
import json


# Load all the metadata about prior subjects
with open('subinfo.json') as f:
    subjects = json.load(f)
    
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

with open('subinfo.json', "w") as f:
    json.dump(subjects, f)
