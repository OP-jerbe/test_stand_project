import configparser

def load_config(file_name:str) -> dict:
     config_data = configparser.ConfigParser()
     config_data.read(file_name)
     return config_data

def find_comport_device(config_data:list, header:str) -> tuple:
     device = config_data.get(header, 'device')
     address = config_data.get(header, 'com_port')
     return device, address

def find_IP_device(config_data:list, header:str) -> tuple:
     device = config_data.get(header, 'device')
     address = config_data.get(header, 'IPaddress')
     return device, address