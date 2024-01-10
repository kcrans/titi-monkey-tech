
# Titi Monkey Technology 
![titi_pic](https://github.com/kcrans/titi-monkey-tech/assets/69497802/65a4addb-b091-4382-8bd2-8570fa942877)

A cross-platform python application for running reaction-based experiments with non-human primates.

## Getting Started

1. Install the latest version of [PsychoPy](https://www.psychopy.org/download.html) on your platform of choice. 

2. Within the PsychoPy application, go to the monitor center and enter your chosen monitor's specifications (this isn't necessarily required, but is recommended for proper stimuli sizing). 

<img width="941" alt="Screen Shot 2022-10-11 at 2 01 42 PM" src="https://user-images.githubusercontent.com/69497802/195198905-cfdb73cd-2c53-4774-976e-1894a4b470ea.png">

3. Using a PsychoPy (or any text-editor ), open **program_specs.py**. Set the `monitor_name` variable to the name of the monitor you added to the monitor center. As we are using fullscreen mode within PsychoPy, the 'window_size' will be overridden, but if you enter the exact screen resolution as your monitor you will avoid an error message during runtime. Set `touch_screen` to `True` or `False` depending on if you are using a mouse or touch-enabled screen. `shape_size` can take on values between 0.0 and 1.0 and scales the size of each stimuli object within the window. Run **shape_test.py** to get a feel for how this scaling factor applies to each different shape.

4. In this application, parameters for the various experiments are tied to specific subjects. So in order to run your first experiment you need to add at least one subject with all of its parameters set. Open and run **changeParameters.py** from within PsychoPy. A gui dialog will pop up. Click on "NEW Subject" from the drop down menu and then click ok.

<img width="1440" alt="screenshot_change_1" src="https://user-images.githubusercontent.com/69497802/196556289-d0aa4df9-5500-48ea-9870-6f41b316ba7c.png">

Now you will be presented with the parameter customization screen. You will first need to enter a name for the subject. Parameters are grouped according to their corresponding phases, with global values at top. Each field has a default value, which can be changed by editing **changeParameters.py** if you wish.

<img width="1440" alt="screenshot_change_2" src="https://user-images.githubusercontent.com/69497802/196557148-8afd6899-9a5f-4fd2-96b5-f7738db3bb79.png">

5. Now we are ready to run some trials. Open **main.py** within PsychoPy and hit run. Select a subject and then select a mode and you are ready to start.

6. Results will be stored in a single csv file titled **titi_monkey_data.csv**. After each run of a training session or experiment, results will be appended to this file.

## Tips and Things to Note

- Press escape at any time during a phase 0 (circle training) run to exit the program. During any of the other training types (including experiments), press escape once the stimulus has been displayed after the hold phase delay.
- You can change the condition of a subject and the session time in the second dialog of **main.py** without having to run the parameter modification utility.


## Architecture Overview

### changeParameters.py and subinfo.json

All parameters are stored in a json file which is structured as a dictionary with top level keys consisting of the names (strings) of all the current test subjects. The sub dictionaries consist of global cross-phase parameters and specific parameters for each phase.
