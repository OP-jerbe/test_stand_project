import sys
from rfgenerator_control import RFGenerator
from ini_reader import load_config
import configparser
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QCheckBox, QLineEdit, QLabel
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.simulate = True

        if not self.simulate:
            self.ini_file = 'hyperionTestStandControl.ini'
            self.rfg_com_port = load_config(self.ini_file, 'RFGenerator')
            self.resource_name = f'ASRL{self.rfg_com_port}::INSTR'
            self.rfg = RFGenerator(self.resource_name)

        self.setWindowTitle("VRG Control")
        self.setWindowIcon(QIcon('./vrg_icon.ico'))
        
        # Enable switch
        self.toggle_switch_label = QLabel('Enable RF', self)
        self.toggle_switch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toggle_switch = QCheckBox("Enable", self)
        self.toggle_switch.setChecked(False)
        self.toggle_switch.stateChanged.connect(self.on_toggle)
        self.toggle_switch.setStyleSheet("""
            QCheckBox {
                width: 50px;
                height: 20px;
                border: 2px solid #999999;
                border-radius: 10px;
                background: #e0e0e0;
            }
            QCheckBox:checked {
                background: #76b041;
                border: 2px solid #76b041;
            }
            QCheckBox:indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox:indicator:checked {
                background: white;
            }
        """)
        
        # Frequency setting
        self.top_freq_label = QLabel('Frequency (MHz)', self)
        self.freq_setting_label = QLabel('Frequency = 00.00 MHz', self)
        self.freq_setting_input = QLineEdit(self)
        self.freq_setting_input.setMaxLength(5)
        self.freq_setting_input.setPlaceholderText('Input Frequency Setting')
        
        # Power setting
        self.top_power_label = QLabel('Power (W)', self)
        self.power_setting_label = QLabel('Power = 0 W', self)
        self.power_setting_input = QLineEdit(self)
        self.power_setting_input.setMaxLength(4)
        self.power_setting_input.setPlaceholderText('Input Power Setting')
        
        # Set up layout
        toggle_switch_layout = QVBoxLayout()
        toggle_switch_layout.addWidget(self.toggle_switch_label)
        toggle_switch_layout.addWidget(self.toggle_switch)
        
        freq_layout = QVBoxLayout()
        freq_layout.addWidget(self.top_freq_label)
        freq_layout.addWidget(self.freq_setting_input)
        freq_layout.addWidget(self.freq_setting_label)
        freq_layout.setContentsMargins(10, 3, 10, 3)
        
        power_layout = QVBoxLayout()
        power_layout.addWidget(self.top_power_label)
        power_layout.addWidget(self.power_setting_input)
        power_layout.addWidget(self.power_setting_label)
        power_layout.setContentsMargins(10, 3, 10, 3)

        main_layout = QHBoxLayout()
        main_layout.addLayout(toggle_switch_layout)
        main_layout.addLayout(freq_layout)
        main_layout.addLayout(power_layout)
        main_layout.setContentsMargins(10, 10, 10, 10) # Set margins (left, top, right, bottom)
        
        container = QWidget()
        container.setLayout(main_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

        # Connect QLineEdit's returnPressed signal to the update_label method with arguments
        # A lambda function is required since arguments must be passed to the update_label method
        self.freq_setting_input.returnPressed.connect(
            lambda: self.update_setting(self.freq_setting_input,
                                      self.freq_setting_label,
                                      param='Frequency',
                                      unit='MHz'
            )
        )

        self.power_setting_input.returnPressed.connect(
            lambda: self.update_setting(self.power_setting_input,
                                      self.power_setting_label,
                                      param='Power',
                                      unit='W'
            )
        )
        
        self.freq_setting_input.focusInEvent = self.clear_text
        self.freq_setting_input.focusOutEvent = self.restore_text_if_empty

        self.power_setting_input.focusInEvent = self.clear_text
        self.power_setting_input.focusOutEvent = self.restore_text_if_empty

    def clear_text(self, event, input_line:QLineEdit):
        # Clear the text when the line eit gains focus
        self.last_input = self.input_line.text()
        self.input_line.clear()
        super().focusInEvent()
    
    def restore_text_if_empty(self, event, input_line:QLineEdit):
        # Restore the last input if the current text is empty
        if self.input_line.text() == '':
            self.input_line.setText(self.last_input)
        super().focusOutEvent(event)


    def on_toggle(self, state):
        if state == 2: # checked
            print('Toggle Switch: ON') # replace this with command to enable
            if not self.simulate:
                self.rfg.enable()
        else: # unchecked
            print('Toggle Switch: OFF') # replace this with command to disable
            if not self.simulate
                self.rfg.disable()
    
    def update_setting(self, input_line:QLineEdit, label:QLabel, param:str, unit:str):
        entered_text = input_line.text() # Get text from QLineEdit
        if param == 'Frequency':
            num = float(entered_text)
            num_as_str = f'{num:.2f}'
            label.setText(f'{param} = {num_as_str} {unit}') # Set text to QLabel
            if not self.simulate
                self.rfg.set_frequency(num)
        elif param == 'Power':
            num = float(entered_text)
            num_as_str = f'{int(num)}'
            label.setText(f'{param} = {num_as_str} {unit}') # Set text to QLabel
            if not self.simulate
                self.rfg.set_power(int(num))
        else:
            pass

        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    




















# =============================================================================
# def load_config(file_name):
#     config = configparser.ConfigParser()
#     config.read(file_name)
#     rf_com_port = config.get('RFGenerator', 'COMPort')
#     return rf_com_port
# 
# def main():
#     # Load the COM Port from the ini file
#     ini_file = 'hyperionTestStandControl.ini'
#     rfg_com_port = load_config(ini_file)
#     
#     resource_name = f'ASRL{rfg_com_port}::INSTR'
#     rfg = RFGenerator(resource_name)
#     
#     # Ping the VRG to see if it's talking
#     rfg.ping_device()
#     
#     # Get Frequency and power settings
#     rfg.get_frequency()
#     rfg.get_power_setting()
#     
#     # Change Frequency and Power settings
#     rfg.set_frequency(40.65)
#     rfg.set_power(800)
#     
#     # Get new frequency and power settings
#     rfg.get_frequency()
#     rfg.get_power_setting()
#     
#     
#     # close the connection
#     rfg.close()
# 
# 
# if __name__ == '__main__':
#     main()
# =============================================================================
