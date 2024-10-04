
class RFGenerator:
    def __init__(self):
        self.product = 'VRG'
        self.enabled = False
        self.freq = 0
        self.power_setting = 0
        self.forward_power = 0
        self.refl_power = 0

    def enable(self):
        self.enabled = True
        print('RF enabled!')
        return self.enabled

    def disable(self):
        self.enabled = False
        self.set_power(0) # simulate VRG output power turning off
        self.forward_power = 0 
        self.refl_power = 0 
        print('RF disabled!')
        return self.enabled

###############################################################################
############################# getter methods ##################################
###############################################################################

    def get_frequency(self):
        """Method to ask RF generator what the frequency setting is."""
        return self.freq

    def get_power_setting(self):
        """Method to ask RF generator what the power setting is."""
        return self.power_setting

    def get_refl_power(self):
        """Method to ask RF generator how much reflected power is coming back"""
        if not self.enabled:
            return self.refl_power
        else:
            self.refl_power = 5 # simulate VRG reflected power
        return self.refl_power

    def get_forward_power(self):
        if not self.enabled:
            return self.forward_power
        else:
            self.forward_power = self.power_setting + self.refl_power
            return self.forward_power
    
    def get_absorbed_power(self):
        return self.forward_power - self.refl_power

###############################################################################
############################# setter methods ##################################
###############################################################################
        
    def set_frequency(self, freq: float):
        self.freq = freq
    
    def auto_tune(self):
        if self.enabled:
            print('VRG auto tuned')
        else:
            pass

    def set_power(self, power: int):
        if power > 800:
            print(f'{power} W is not allowed. Power set to 800 W')
            self.power_setting = 800 # limit power to 800 W
        elif power < 0:
            print(f'{power} is not an allowed setting. Power set to 0 W')
            self.power_setting = 0 # do not accept negative numbers
        else:
            self.power_setting = power
