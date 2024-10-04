
import ammeter_control as amm
import pressure_gauge_control as pg
import rfgenerator_control as rfg


# create an rf class
rf = rfg.RFGenerator()
print(f'RF Generator type: {rf.product}')

rf.set_frequency(40.01)
rf.set_power(800)

frequency_var = rf.get_frequency()
print(f'frequency_var = {frequency_var} MHz')

power_setting_var = rf.get_power_setting()
print(f'power_setting_var = {power_setting_var} W')

forward_power_var = rf.get_forward_power()
print(f'forward_power_var = {forward_power_var} W')

refl_power_var = rf.get_refl_power()
print(f'refl_power_var = {refl_power_var} W')



rf.enable()

forward_power_var = rf.get_forward_power()
print(f'forward_power_var = {forward_power_var} W')

refl_power_var = rf.get_refl_power()
print(f'refl_power_var = {refl_power_var} W')

absorbed_power_var = rf.get_absorbed_power()
print(f'absorbed_power_var = {absorbed_power_var} W')



rf.disable()

forward_power_var = rf.get_forward_power()
print(f'forward_power_var = {forward_power_var} W')

refl_power_var = rf.get_refl_power()
print(f'refl_power_var = {refl_power_var} W')

absorbed_power_var = rf.get_absorbed_power()
print(f'absorbed_power_var = {absorbed_power_var} W')