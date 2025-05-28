import pyvisa


class VRG:
    def __init__(
        self, resource_name: str
    ) -> None:  # probably set the resource name in .ini file
        self.rm = pyvisa.ResourceManager('@py')
        self.instrument = self.rm.open_resource(resource_name)

        # Get the valid frequency range in MHz

        self.min_tune_freq = self.read_min_tune_freq()
        self.max_tune_freq = self.read_max_tune_freq()
        self.max_power_setting = 1000

    def query_command(self, command) -> None:
        self.instrument.query(command)  # type:ignore

    def write_command(self, command) -> None:
        self.instrument.write(command)  # type:ignore

    def write_raw_command(self, command) -> None:
        self.instrument.write_raw(command)  # type:ignore

    def read_command(self) -> str | None:
        try:
            response: str = self.instrument.read()  # type:ignore
            print(f'Received response: {response}')  # Debugging info
            return response
        except pyvisa.VisaIOError as e:
            print(f'Error reading response: {e}')
            return None

    def ping(self) -> str | None:
        command = b'!\n'
        self.write_raw_command(command)
        response: str | None = self.read_command()
        return response

    def read_frequency(self) -> float:
        """returns the frequency setting in MHz"""
        command: str = 'RQ'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return float(response.strip(command).strip('\r\n')) * 1e-3
        else:
            return 0.00

    def read_power_setting(self) -> int:
        """returns the power setting in watts"""
        command = 'RO'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return int(response.strip(command).strip('\r\n'))
        else:
            return 0

    def read_min_tune_freq(self) -> float:
        """returns the minimum allowable freq setting in MHz"""
        command = 'R1'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return float(response.strip(command).strip('\r\n')) * 1e-3
        else:
            return 0.00

    def read_max_tune_freq(self) -> float:
        """returns the maximum allowable freq setting in MHz"""
        command = 'R2'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return float(response.strip(command).strip('\r\n')) * 1e-3
        else:
            return 0.00

    def read_forward_power(self) -> int:
        """returns the forward power in watts"""
        command = 'RF'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return int(response.strip(command).strip('\r\n'))
        else:
            return 0

    def read_reflected_power(self) -> int:
        """returns the reflected power in watts"""
        command = 'RR'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return int(response.strip(command).strip('\r\n'))
        else:
            return 0

    def read_absorbed_power(self) -> float:
        """returns the absorbed power in watts"""
        command = 'RB'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            return float(response.strip(command).strip('\r\n'))
        else:
            return 0.0

    def read_factory_info(self) -> tuple:
        """returns the product serial number, number of reboots, operating hours and enabled hours"""
        command = 'RI'
        self.write_command(command)
        response: str | None = self.read_command()
        if response is not None:
            split_response: list = response.split()
            serial_number: str = split_response[0]
            reboots: int = int(split_response[1])
            op_hours: int = int(split_response[2])
            enabled_hours: int = int(split_response[3])
            return (
                serial_number.strip(command),
                int(reboots),
                int(op_hours),
                int(enabled_hours),
            )
        else:
            return ('unknown', '0', '0', '0', '0')

    def enable_RF(self) -> None:
        command = 'ER'
        self.write_command(command)
        self.read_command()

    def disable_RF(self) -> None:
        command = 'DR'
        self.write_command(command)
        self.read_command()

    def set_forward_mode(self) -> None:
        command = 'PM0'
        self.write_command(command)
        self.read_command()

    def set_absorbed_mode(self) -> None:
        command = 'PM1'
        self.write_command(command)
        self.read_command()

    def autotune(self) -> None:
        command = 'TW'
        self.write_command(command)
        self.read_command()

    def narrow_autotune(self) -> None:
        command = 'TT'
        self.write_command(command)

    def set_rf_power(self, power: int) -> None:
        # Type validation
        if not isinstance(power, int):
            raise TypeError(f'Expected an integer, but got {type(power).__name__}')
        # Range validation
        if power < 0 or power > self.max_power_setting:
            raise ValueError(
                f'Input {power} is out of bounds. Must be between 0 and {self.max_power_setting}.'
            )

        command = f'SP{power:04}'  # ensures that the integer power is always represented as a 4-digit string, padded with leading zeros if necessary
        self.write_command(command)
        self.read_command()

    def set_freq(self, freq: int | float) -> None:
        # Type validation
        if not isinstance(freq, int | float):
            raise TypeError(f'Expected an float or int, but got {type(freq).__name__}')

        # Get the valid frequency range in MHz
        min_freq = self.min_tune_freq
        max_freq = self.max_tune_freq

        # Range validation
        if not (min_freq <= freq <= max_freq):
            raise (
                ValueError(
                    f'Frequency {freq} MHz is out of range. Must be between {min_freq:.2f} and {max_freq:.2f} MHz.'
                )
            )

        freq_kHz = int(freq * 1000)
        command = f'SF{freq_kHz:05d}'
        self.write_command(command)
        self.read_command()

    def close(self) -> None:
        self.instrument.close()


# Read command examples
# =============================================================================
# print(vrg.query('RQ')) # Read Frequency returns "RQ40650" for 40.65 MHz
# print(vrg.query('RO')) # Read Power Setting returns "RO0800" for 800 W
# print(vrg.query('R1')) # Read Min tune frequency returns "R125000"
# print(vrg.query('R2')) # Read Max tune frequency retunrs "R242000"
# print(vrg.query('RF')) # Read Forward Power returns "RF0000" when not enabled
# print(vrg.query('RR')) # Read Reflected Power returns "RF0000" when not enabled
# print(vrg.query('RB')) # Read Absorbed Power returns "RB0000.1" when not enabled
# print(vrg.query('RI')) # Read Factory Information returns "RI607 00171 022426 017180 00000 00000" 607 is serial number, 171 is num of reboots 22426 is operating hours, 17180 is enabled hours, zeros are unimplementd options
# =============================================================================

# Write command examples
# =============================================================================
# vrg.write('ER') # Enable RF
# vrg.write('DR') # Disable RF
# vrg.write('PM0') # Set Power Control Mode to Forward Power Mode
# vrg.write('PM1') # Set Power Control Mode to Absorbed Power Mode
# vrg.write('TW') # Trigger a wide range auto tune (typically used)
# vrg.write('TT') # Trigger an narrow range auto tune
# vrg.write('SP0600') # Set RF power to 600 W
# vrg.write('SP0800') # Set RF power to 800 W
# vrg.write('SF41000') # Set frequency to 41.00 MHz
# vrg.write('SF40650') # Set frequency to 40.65 MHz
# =============================================================================
