import threading


class RFGenerator:
    def __init__(self, resource_name, rf_device_type=None):
        self.set_rf_device(rf_device_type, resource_name)
        self.enabled = False
        self.freq = 0
        self.power_setting = 0
        self.forward_power = 0
        self.refl_power = 0
        self.absorbed_power = 0.0
        self.lock = threading.Lock()

    def set_rf_device(self, rf_device_type, resource_name):
        device = None
        accepted_devices = ['VRG']
        # The first conditional statement is here to add RF generator types in the future
        if rf_device_type in accepted_devices:
            if rf_device_type == 'VRG':
                from src.vrg.vrg_api import VRG as device
        else:
            raise ValueError(
                f'Unknown RF device type: {rf_device_type}. Accepted devices: {", ".join(accepted_devices)}'
            )

        if device is None:
            raise RuntimeError('Device class could not be imported')

        self.rf_device = device(resource_name)

    def ping_device(self):
        with self.lock:
            return self.rf_device.ping()

    def enable(self):
        with self.lock:
            self.rf_device.enable_RF()
            self.enabled = True

    def disable(self):
        with self.lock:
            self.rf_device.disable_RF()
            self.enabled = False

    def close(self):
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

    def set_frequency(self, freq: float):
        with self.lock:
            self.rf_device.set_freq(freq)

    def auto_tune(self):
        with self.lock:
            self.rf_device.autotune()

    def set_power(self, power: int):
        with self.lock:
            self.rf_device.set_rf_power(power)
