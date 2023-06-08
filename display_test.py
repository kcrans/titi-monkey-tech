from psychopy import prefs, monitors
#prefs.general['winType'] = 'pygame'
from psychopy import visual


mon = monitors.Monitor("macbook")

mywin = visual.Window(size=[1600, 900], fullscr=True, color="black", monitor=mon, units="height")

print(prefs)