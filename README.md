
# Titi Monkey Technology 

## Getting Started

1. Install the latest version of [PsychoPy](https://www.psychopy.org/download.html) on your platform of choice. 

2. Within the PsychoPy application, go to the monitor center and enter your chosen monitor's specifications (this isn't necessarily required, but is recommended for proper stimuli sizing). 

<img width="941" alt="Screen Shot 2022-10-11 at 2 01 42 PM" src="https://user-images.githubusercontent.com/69497802/195198905-cfdb73cd-2c53-4774-976e-1894a4b470ea.png">

3. Go to the 


## Architecture Overview

### changeParameters.py and subinfo.json

All parameters are stored in a json file which is structured as a dictionary with top level keys consisting of the names (strings) of all the current test subjects. The sub dictionaries consist of global cross-phase parameters and specific parameters for each phase.

