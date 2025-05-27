from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import (
    QDoubleValidator,
    QFocusEvent,
    QRegularExpressionValidator,
    QValidator,
)
from PySide6.QtWidgets import QLineEdit


class CustomLineEdit(QLineEdit):
    def __init__(self, name: str, main_window, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Set attributes
        self.main_window = main_window
        self.name = name
        self.last_input = self.text()  # Store the last input

        # Set the data entry validations
        # Allow only digits (0-9) and periods (.) in the entry box
        regex = QRegularExpression(
            r'[0-9.]*'
        )  # Regular expression for numbers and period
        regex_validator = QRegularExpressionValidator(regex, self)
        self.setValidator(regex_validator)

        # Set the numeric limits and decimal precision
        power_double_validator = QDoubleValidator(
            0.0, 1000.0, 3
        )  # (min value, max value, decimals)
        freq_double_validator = QDoubleValidator(25.00, 42.00, 3)
        power_double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        freq_double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        # Setting all validators: First limit characters, then the check numeric ranges
        self.regex_validator = regex_validator
        self.power_double_validator = power_double_validator
        self.freq_double_validator = freq_double_validator

    # Currently this does nothing useful but, if self.clear() is uncommented the entry box will clear when selected.
    def focusInEvent(self, arg__1: QFocusEvent) -> None:
        self.last_input = self.text()  # Store the current text when focused
        super().focusInEvent(arg__1)  # Call the base class method
        # self.clear()  # Clear the text when the focus is set on the entry box

    def focusOutEvent(self, arg__1: QFocusEvent) -> None:
        # Check if the box is empty
        if self.text() == '':
            print('restored last input')
            self.setText(self.last_input)  # Restore the last input if empty
            super().focusOutEvent(arg__1)
            return

        # Validate character restrictions first (digits and periods only)
        validation_result = self.regex_validator.validate(self.text(), 0)
        if isinstance(validation_result, tuple) and len(validation_result) == 3:
            regex_state, _, _ = validation_result
        else:
            print('Regex validation did not return the expected tuple structure.')
            return

        if regex_state != QValidator.State.Acceptable:
            print('Invalid characters entered. Restoring last input.')
            self.setText(self.last_input)
            super().focusOutEvent(arg__1)
            return

        # Validate numeric range and decimal limits depending on which input box is being edited.
        # if the input is acceptable, update the setting.
        if self.name == 'freq':
            validation_result = self.freq_double_validator.validate(self.text(), 0)
            if isinstance(validation_result, tuple) and len(validation_result) == 3:
                double_state, _, _ = validation_result
            else:
                print('Double validation did not return the expected tuple structure')
                return

            if double_state != QValidator.State.Acceptable:
                print('Value out of range or too many decimals.')
                self.setText(self.last_input)
                super().focusOutEvent(arg__1)
                return
            self.main_window.update_setting(
                input_line=self.main_window.freq_setting_input,
                param='Frequency',
                unit='MHz',
            )
        elif self.name == 'power':
            validation_result = self.power_double_validator.validate(self.text(), 0)
            if isinstance(validation_result, tuple) and len(validation_result) == 3:
                double_state, _, _ = validation_result
            else:
                print('Double validation did not return the expected tuple structure')
                return

            if double_state != QValidator.State.Acceptable:
                print('Value out of range or too many decimals.')
                self.setText(self.last_input)
                super().focusOutEvent(arg__1)
                return
            self.main_window.update_setting(
                input_line=self.main_window.power_setting_input, param='Power', unit='W'
            )

        super().focusOutEvent(arg__1)  # Call the base class method
