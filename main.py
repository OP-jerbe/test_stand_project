import sys
from rfgenerator_control import RFGenerator
from ini_reader import load_config
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QCheckBox, QLineEdit, QLabel, QPushButton
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout


class CustomLineEdit(QLineEdit):
    def __init__(self, name:str, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.name = name
        self.last_input = self.text()  # Store the last input

    def focusInEvent(self, event):
        self.last_input = self.text()  # Store the current text when focused
        super().focusInEvent(event)  # Call the base class method
        self.clear()  # Clear the text

    def focusOutEvent(self, event):
        if self.text() == '':
            print('restored last input')
            self.setText(self.last_input)  # Restore the last input if empty
        elif self.text() != '' and self.name == 'freq':
            self.main_window.update_setting(
                input_line=self.main_window.freq_setting_input,
                label=self.main_window.freq_setting_label,
                param='Frequency',
                unit='MHz'
            )
        elif self.text() != '' and self.name == 'power':
            self.main_window.update_setting(
                input_line=self.main_window.power_setting_input,
                label=self.main_window.power_setting_label,
                param='Power',
                unit='W'
            )
        super().focusOutEvent(event)  # Call the base class method
    
    def restore_text(self):
        if self.text() == '':
            self.setText(self.last_input)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.simulation = False

        # Install event filter to capture all mouse clicks
        self.installEventFilter(self)

        if not self.simulation:
            self.ini_file = 'hyperionTestStandControl.ini'
            self.rfg_com_port = load_config(self.ini_file, 'RFGenerator')
            self.resource_name = f'ASRL{self.rfg_com_port}::INSTR'
            self.rfg = RFGenerator(self.resource_name)

        if not self.simulation:
            self.setWindowTitle("VRG Control")
        else:
            self.setWindowTitle('VRG Control - (simulation)')
        self.setWindowIcon(QIcon('./vrg_icon.ico'))
        
        # Enable switch
        self.enable_switch = QCheckBox('Enable RF', self)
        self.enable_switch.setChecked(False)
        self.enable_switch.stateChanged.connect(self.on_toggle)
        self.enable_switch.setStyleSheet("""
            QCheckBox {
                width: 75px;
                height: 20px;
                border: 2px solid #999999;
                border-radius: 10px;
                background: #e0e0e0;
                text-align: center;
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
        self.top_freq_label = QLabel('Frequency (MHz)')
        if not self.simulation:
            self.freq_setting_label = QLabel(f'Frequency = {self.rfg.get_frequency():.2f} MHz')
        else:
            self.freq_setting_label = QLabel('Frequency = 00.00 MHz')
        self.freq_setting_input = CustomLineEdit(name='freq', main_window=self)
        self.freq_setting_input.setMaxLength(5)
        self.freq_setting_input.setPlaceholderText('Input Frequency Setting')
        
        # Power setting
        self.top_power_label = QLabel('Power (W)')
        if not self.simulation:
            self.power_setting_label = QLabel(f'Power = {self.rfg.get_power_setting()} W')
        else:
            self.power_setting_label = QLabel('Power = 0 W')
        self.power_setting_input = CustomLineEdit(name='power', main_window=self)
        self.power_setting_input.setMaxLength(4)
        self.power_setting_input.setPlaceholderText('Input Power Setting')
        
        # Auto tune
        self.autotune_button = QPushButton('Autotune')

        # Set up layout
        es_and_at_layout = QVBoxLayout()
        es_and_at_layout.addWidget(self.enable_switch)
        es_and_at_layout.addWidget(self.autotune_button)
        
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
        main_layout.addLayout(es_and_at_layout)
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
            lambda: [
                # self.update_setting(
                #     self.freq_setting_input,
                #     self.freq_setting_label,
                #     param='Frequency',
                #     unit='MHz'
                # ),
                self.freq_setting_input.clearFocus()
            ]
        )

        self.power_setting_input.returnPressed.connect(
            lambda: [
                # self.update_setting(
                #     self.power_setting_input,
                #     self.power_setting_label,
                #     param='Power',
                #     unit='W'
                # ),
                self.power_setting_input.clearFocus()
            ]
        )

        self.autotune_button.clicked.connect(self.autotune_clicked)


    def eventFilter(self, source, event):
        # Capture all mouse button press events
        if event.type() == QEvent.MouseButtonPress:
            focused_widget = QApplication.focusWidget() # Get the currently focused widget
            focused_widget.clearFocus()  # clear focus from the current QLineEdit
        return super().eventFilter(source, event)


    def on_toggle(self, state):
        if state == 2: # checked
            print('Toggle Switch: ON') # replace this with command to enable
            if not self.simulation:
                self.rfg.enable()
        else: # unchecked
            print('Toggle Switch: OFF') # replace this with command to disable
            if not self.simulation:
                self.rfg.disable()


    def update_setting(self, input_line:CustomLineEdit, label:QLabel, param:str, unit:str):
        entered_text = input_line.text() # Get text from CustomLineEdit
        num = float(entered_text)

        if not self.simulation:
            # Code to run if connected to RF generator
            if param == 'Frequency':
                num_as_str = f'{num:.2f}'
                input_line.setText(num_as_str)
                self.rfg.set_frequency(num) # tell RF generator to set the frequency to num
                freq = self.rfg.get_frequency() # ask RF generator what it's frequency setting is
                label.setText(f'{param} = {freq:.2f} {unit}')
            elif param == 'Power':
                num_as_str = f'{int(num)}'
                input_line.setText(num_as_str)
                self.rfg.set_power(int(num)) # tell RF generator to set the frequency to num
                power = self.rfg.get_power_setting() # ask RF generator what it's frequency setting is
                label.setText(f'{param} = {power} {unit}')
        else:
            # Code to run if in simulation mode
            if param == 'Frequency':
                num_as_str = f'{num:.2f}'
            elif param == 'Power':
                num_as_str = f'{int(num)}'
            input_line.setText(num_as_str) # Set text of the input box
            label.setText(f'{param} = {num_as_str} {unit}') # Set text to QLabel


    def autotune_clicked(self):
        if not self.simulation:
            self.rfg.auto_tune()
            new_freq = self.rfg.get_frequency()
            self.freq_setting_input.setText(f'{new_freq}')
            self.freq_setting_label.setText(f'Frequency = {new_freq:.2f} MHz')
        print('Autotuned!')

        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
