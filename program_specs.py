# ** Universal Parameters **
"""
These parameter values are used in all programs for the project
"""
monitor_name = 'macbook'
# Put the name of your monitor in the quotes above
window_size = [1440, 900]
touch_screen = True
shape_size = 0.6 # Scale for the size of all shape stimuli
font_size = 50 # Font size for touchsrcreen mode
file_name = "titi_monkey_data.csv" # Name of file storing results
style_sheet = f"""
QWidget      {{
        font-size: {font_size}px;
        }}
QComboBox {{
    border: 1px solid gray;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}}

QComboBox:editable {{
    background: white;
}}

QComboBox:!editable, QComboBox::drop-down:editable {{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
}}

QComboBox:on {{ /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}}

/* Background color of popup-list.*/ 
QComboBox QListView{{
    background-color:white;
    border:1px solid gray;
}}
/* Needed to complete the rule set. */
QComboBox::item:alternate {{
    background: white;
}}
/* Color of the selected list item. */
QComboBox::item:selected {{
    border: 1px solid transparent;
    background:yellow;
}}

QComboBox::indicator{{
    background-color:transparent;
    selection-background-color:transparent;
    color:transparent;
    selection-color:transparent;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}}

QComboBox::down-arrow {{
    image: url(1downarrow.png);
}}

QComboBox::down-arrow:on {{ /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
    }}
QLineEdit {{
    border: 2px solid gray;
    border-radius: 10px;
    padding: 0 8px;
    background: yellow;
    selection-background-color: darkgray;
}}
        """
