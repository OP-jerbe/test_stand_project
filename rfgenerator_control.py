
from vrg_api import VRG as device

class RFGenerator():
    def __init__(self, resource_name):
        self.rf_device = device(resource_name)
        self.enabled = False
        self.freq = 0
        self.power_setting = 0
        self.forward_power = 0
        self.refl_power = 0
        
    def ping_device(self):
        return self.rf_device.ping()
    
    def enable(self):
        self.rf_device.enable_RF()
        self.enabled = True

    def disable(self):
        self.rf_device.disable_RF()
        self.enabled = False
    
    def close(self):
        self.rf_device.close()

###############################################################################
############################# getter methods ##################################
###############################################################################

    def get_frequency(self) -> float:
        """Method to ask RF generator what the frequency setting is."""
        self.freq = self.rf_device.read_frequency()
        return self.freq

    def get_power_setting(self) -> int:
        """Method to ask RF generator what the power setting is."""
        self.power_setting = self.rf_device.read_power_setting()
        return self.power_setting

    def get_refl_power(self) -> int:
        """Method to ask RF generator how much reflected power is coming back"""
        self.refl_power = self.rf_device.read_reflected_power()
        return self.refl_power

    def get_forward_power(self) -> int:
        self.forward_power = self.rf_device.read_forward_power()
        return self.forward_power
    
    def get_absorbed_power(self) -> int:
        forward_power = self.rf_device.read_forward_power()
        reflected_power = self.rf_device.read_reflected_power()
        return forward_power - reflected_power

###############################################################################
############################# setter methods ##################################
###############################################################################
        
    def set_frequency(self, freq: float):
        self.rf_device.set_freq(freq)
    
    def auto_tune(self):
        self.rf_device.autotune()

    def set_power(self, power: int):
        self.rf_device.set_rf_power(power)
