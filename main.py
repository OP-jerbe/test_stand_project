from rfgenerator_control import RFGenerator
import configparser


def load_config(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    com_port = config.get('RFGenerator', 'COMPort')
    return com_port

def main():
    # Load the COM Port from the ini file
    ini_file = 'hyperionTestStandControl.ini'
    com_port = load_config(ini_file)
    
    vrg_resource = f'ASRL{com_port}::INSTR'
    
    resource_name = vrg_resource # set this with ini file???
    rfg = RFGenerator(resource_name)
    
    # Ping the VRG to see if it's talking
    ping = rfg.ping_device()
    freq_start = rfg.get_frequency()
    power_start = rfg.get_power_setting()
    rfg.set_frequency(40.65)
    rfg.set_power(800)
    freq_end = rfg.get_frequency()
    power_end = rfg.get_power_setting()
    
    
    # close the connection
    rfg.close()


if __name__ == '__main__':
    main()
