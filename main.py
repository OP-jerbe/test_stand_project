import sys
from CustomLineEdit import CustomLineEdit
from rfgenerator_control import RFGenerator
from ini_reader import load_config, find_comport_device
from PySide6.QtCore import QEvent
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PySide6.QtWidgets import QCheckBox, QLabel, QPushButton
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.simulation = False

        # Install event filter to capture all mouse clicks
        self.installEventFilter(self)

        # Handle ini file and load parameters
        self.ini_file = 'hyperionTestStandControl.ini'
        self.config_data = load_config(self.ini_file)
        self.rf_device, self.rf_com_port = find_comport_device(self.config_data, 'RFGenerator')

        try:
            self.resource_name = f'ASRL{self.rf_com_port}::INSTR'
            self.rfg = RFGenerator(self.resource_name, self.rf_device)
        except Exception as e:
            #print(f'Exception: {e}')
            print('Could not connect to RF device. App in simulation mode.')
            self.simulation = True

        
        self.create_gui()

        if not self.simulation:
            from PySide6.QtCore import QTimer
            from rf_data_acquisition import DataAcquisition
            
            # Set the refresh rate and use it for both data acquisition and GUI update
            self.refresh_rate = 1000  # 1000ms = 1 second
            
            # Data acquisition setup
            self.data_acquisition = DataAcquisition(self.rfg, self.refresh_rate / 1000) if self.rfg else None
            self.data_acquisition.start()

            # Timer to update the GUI with data from the RF device
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_display)
            self.timer.start(self.refresh_rate)

    def update_display(self):
        # Only run if a device is connected
        if not self.simulation:
            """
            Update the display with the latest data from the RF device.
            """
            data = self.data_acquisition.get_data()
            timestamp = data['timestamp']
            
            self.forward_power_label.setText(f"Forward Power: {data['forward_power']:.2f} W")
            self.reflected_power_label.setText(f"Reflected Power: {data['reflected_power']:.2f} W")
            self.absorbed_power_label.setText(f"Absorbed Power: {data['absorbed_power']:.2f} W")
            self.frequency_label.setText(f"Frequency: {data['frequency']:.2f} MHz")

    def closeEvent(self, event):
        # Confirm the user wants to exit the application.
        reply = QMessageBox.question(self, 'Confirmation',
                                     "Are you sure you want to close the window?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

        # Only run if a device is connected.    
        if not self.simulation:
            """
            Stop the data acquisition when the window is closed.
            """
            self.data_acquisition.stop()
            event.accept()

    def create_gui(self) -> None:
        if not self.simulation:
            self.setWindowTitle("VRG Control")
        else:
            self.setWindowTitle('VRG Control - (simulation)')
        self.setWindowIcon(QIcon('./vrg_icon.ico'))

        # Create enable rf switch
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
        
        # Create frequency setting labels and input boxes
        self.top_freq_label = QLabel('Frequency (MHz)')
        if not self.simulation:
            self.freq_setting_label = QLabel(f'Frequency = {self.rfg.get_frequency():.2f} MHz')
        else:
            self.freq_setting_label = QLabel('Frequency = 00.00 MHz')
        self.freq_setting_input = CustomLineEdit(name='freq', main_window=self)
        self.freq_setting_input.setMaxLength(5)
        self.freq_setting_input.setPlaceholderText('Input Frequency Setting')
        
        # Create power setting labels and input boxes
        self.top_power_label = QLabel('Power (W)')
        if not self.simulation:
            self.power_setting_label = QLabel(f'Power = {self.rfg.get_power_setting()} W')
        else:
            self.power_setting_label = QLabel('Power = 0 W')
        self.power_setting_input = CustomLineEdit(name='power', main_window=self)
        self.power_setting_input.setMaxLength(4)
        self.power_setting_input.setPlaceholderText('Input Power Setting')
        
        # Create the autotune button
        self.autotune_button = QPushButton('Autotune')

        # Create labels for displaying power and frequency
        self.forward_power_label = QLabel("Forward Power: 0 W")
        self.reflected_power_label = QLabel("Reflected Power: 0 W")
        self.absorbed_power_label = QLabel("Absorbed Power: 0 W")
        self.frequency_label = QLabel("Frequency: 0 MHz")

        # Set up layout
        fwd_refl_layout = QVBoxLayout()
        fwd_refl_layout.addWidget(self.forward_power_label)
        fwd_refl_layout.addWidget(self.reflected_power_label)

        abs_freq_layout = QVBoxLayout()
        abs_freq_layout.addWidget(self.absorbed_power_label)
        abs_freq_layout.addWidget(self.frequency_label)

        readbacks_layout = QHBoxLayout()
        readbacks_layout.addLayout(fwd_refl_layout)
        readbacks_layout.addLayout(abs_freq_layout)

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

        inputs_layout = QHBoxLayout()
        inputs_layout.addLayout(es_and_at_layout)
        inputs_layout.addLayout(freq_layout)
        inputs_layout.addLayout(power_layout)
        inputs_layout.setContentsMargins(10, 10, 10, 10) # Set margins (left, top, right, bottom)

        main_layout = QVBoxLayout()
        main_layout.addLayout(inputs_layout)
        main_layout.addLayout(readbacks_layout)
        
        container = QWidget()
        container.setLayout(main_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

        # Release the focus from the entry box when the enter button is pressed
        self.freq_setting_input.returnPressed.connect(self.freq_setting_input.clearFocus)
        self.power_setting_input.returnPressed.connect(self.power_setting_input.clearFocus)

        # Send autotune command when the autotune_button is pressed
        self.autotune_button.clicked.connect(self.autotune_clicked)

    def eventFilter(self, source:QMainWindow, event:QMouseEvent) -> bool:
        # Capture all mouse button press events
        if event.type() == QEvent.MouseButtonPress:
            focused_widget = QApplication.focusWidget() # Get the currently focused widget
            if focused_widget is not None:
                focused_widget.clearFocus()  # clear focus from the current focused widget
        return super().eventFilter(source, event)

    def on_toggle(self, state:int) -> None:
        if state == 2: # checked
            print('Toggle Switch: ON') # replace this with command to enable
            if not self.simulation:
                self.rfg.enable()
        else: # unchecked
            print('Toggle Switch: OFF') # replace this with command to disable
            if not self.simulation:
                self.rfg.disable()

    def update_setting(self, input_line:CustomLineEdit, label:QLabel, param:str, unit:str) -> None:
        entered_text: str = input_line.text() # Get text from CustomLineEdit
        num: float = float(entered_text)  # Validate that the input is a float
        if not self.simulation:
            # Code to run if connected to RF generator
            if param == 'Frequency':
                num_as_str: str = f'{num:.2f}'
                input_line.setText(num_as_str)
                self.rfg.set_frequency(num) # tell RF generator to set the frequency to num
                freq: float = self.rfg.get_frequency() # ask RF generator what it's frequency setting is
                label.setText(f'{param} = {freq:.2f} {unit}')
            elif param == 'Power':
                num_as_str: str = f'{int(num)}'
                input_line.setText(num_as_str)
                self.rfg.set_power(int(num)) # tell RF generator to set the frequency to num
                power: int = self.rfg.get_power_setting() # ask RF generator what it's frequency setting is
                label.setText(f'{param} = {power} {unit}')
        else:
            # Code to run if in simulation mode
            if param == 'Frequency':
                num_as_str: str = f'{num:.2f}'
            elif param == 'Power':
                num_as_str: str = f'{int(num)}'
            input_line.setText(num_as_str) # Set text of the input box
            label.setText(f'{param} = {num_as_str} {unit}') # Set text to QLabel

    def autotune_clicked(self) -> None:
        if not self.simulation:
            self.rfg.auto_tune()
            new_freq: float = self.rfg.get_frequency()
            self.freq_setting_input.setText(f'{new_freq}')
            self.freq_setting_label.setText(f'Frequency = {new_freq:.2f} MHz')
        print('Autotuned!')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
