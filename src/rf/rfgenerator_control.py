import threading


class RFGenerator:
    def __init__(self, resource_name: str, rf_device_type: str | None = None) -> None:
        self.set_rf_device(rf_device_type, resource_name)
        self.enabled: bool = False
        self.freq: float = 0
        self.power_setting: int = 0
        self.forward_power: int = 0
        self.refl_power: int = 0
        self.absorbed_power: float = 0.0
        self.lock = threading.Lock()

    def set_rf_device(self, rf_device_type: str | None, resource_name: str) -> None:
        accepted_devices = ['VRG']

        if rf_device_type not in accepted_devices:
            raise ValueError(
                f'Unknown RF device type: {rf_device_type}. Accepted devices: {", ".join(accepted_devices)}'
            )

        if rf_device_type == 'VRG':
            from ..rf.vrg_api import VRG as device

            self.rf_device = device(resource_name)

        if rf_device_type is None:
            raise RuntimeError('Device class could not be imported')

    def ping_device(self) -> str | None:
        with self.lock:
            return self.rf_device.ping()

    def enable(self) -> None:
        with self.lock:
            self.rf_device.enable_RF()
            self.enabled = True

    def disable(self) -> None:
        with self.lock:
            self.rf_device.disable_RF()
            self.enabled = False

    def close(self) -> None:
        with self.lock:
            self.rf_device.close()

    ###############################################################################
    ############################# getter methods ##################################
    ###############################################################################

    def get_frequency(self) -> float:
        """Method to ask RF generator what the frequency setting is."""
        with self.lock:
            self.freq = self.rf_device.read_frequency()
            return self.freq

    def get_power_setting(self) -> int:
        """Method to ask RF generator what the power setting is."""
        with self.lock:
            self.power_setting = self.rf_device.read_power_setting()
            return self.power_setting

    def get_refl_power(self) -> int:
        """Method to ask RF generator how much reflected power is coming back"""
        with self.lock:
            self.refl_power = self.rf_device.read_reflected_power()
            return self.refl_power

    def get_forward_power(self) -> int:
        with self.lock:
            self.forward_power = self.rf_device.read_forward_power()
            return self.forward_power

    def get_absorbed_power(self) -> float:
        with self.lock:
            self.absorbed_power = self.rf_device.read_absorbed_power()
            return self.absorbed_power

    ###############################################################################
    ############################# setter methods ##################################
    ###############################################################################

    def set_frequency(self, freq: float) -> None:
        with self.lock:
            self.rf_device.set_freq(freq)

    def auto_tune(self) -> None:
        with self.lock:
            self.rf_device.autotune()

    def set_power(self, power: int) -> None:
        with self.lock:
            self.rf_device.set_rf_power(power)
