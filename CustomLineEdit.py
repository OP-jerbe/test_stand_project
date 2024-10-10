from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QDoubleValidator, QRegularExpressionValidator, QValidator
from PySide6.QtWidgets import QLineEdit

class CustomLineEdit(QLineEdit):
    def __init__(self, name:str, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set attributes
        self.main_window = main_window
        self.name = name
        self.last_input = self.text()  # Store the last input

        # Set the data entry validations
        # Allow only digits (0-9) and periods (.) in the entry box
        regex = QRegularExpression(r'[0-9.]*')  # Regular expression for numbers and period
        regex_validator = QRegularExpressionValidator(regex, self)
        self.setValidator(regex_validator)

        # Set the numeric limits and decimal precision
        double_validator = QDoubleValidator(0.0, 1000.0, 2) # (min value, max value, decimals)
        double_validator.setNotation(QDoubleValidator.StandardNotation)

        # Setting both validators: First limit characters, then check numeric range
        self.regex_validator = regex_validator
        self.double_validator = double_validator

    def focusInEvent(self, event):
        self.last_input = self.text()  # Store the current text when focused
        super().focusInEvent(event)  # Call the base class method
        # self.clear()  # Clear the text when the focus is set on the entry box

    def focusOutEvent(self, event):
        # Validate character restrictions first (digits and periods)
        regex_state, _, _ = self.regex_validator.validate(self.text(), 0)
        if regex_state != QValidator.Acceptable:
            print("Invalid characters entered. Restoring last input.")
            self.setText(self.last_input)
            super().focusOutEvent(event)
            return
        
        # Validate numeric range and decimal limits
        double_state, _, _ = self.double_validator.validate(self.text(), 0)
        if double_state != QValidator.Acceptable:
            print("Value out of range or too many decimals. Restoring last input.")
            self.setText(self.last_input)
            super().focusOutEvent(event)
            return

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