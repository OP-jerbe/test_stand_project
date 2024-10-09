import configparser

def load_config(file_name:str, header:str) -> str:
     config = configparser.ConfigParser()
     config.read(file_name)
     com_port = config.get(header, 'COMPort')
     print(f'{type(com_port) = }')
     return com_port