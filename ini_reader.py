import configparser
from typing import TypeAlias

ConfigData: TypeAlias = configparser.ConfigParser

def load_config(file_name:str) -> ConfigData:
     config_data = configparser.ConfigParser()
     config_data.read(file_name)
     return config_data

def find_comport_device(config_data: ConfigData, header:str) -> tuple:
     device = config_data.get(header, 'device')
     address = config_data.get(header, 'com_port')
     return device, address

def find_IP_device(config_data: ConfigData, header:str) -> tuple:
     device = config_data.get(header, 'device')
     address = config_data.get(header, 'IPaddress')
     return device, address



if __name__ == '__main__':
     ini_file = 'hyperionTestStandControl.ini'
     config_data = load_config(ini_file)
     rf_device, com_port = find_comport_device(config_data, 'RFGenerator')
     hvps_device, ip = find_IP_device(config_data, 'HVPS')
     print(f'{rf_device = }\n{com_port = }')
     print(f'{hvps_device = }\n{ip = }')