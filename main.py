from rfgenerator_control import RFGenerator
import configparser
from PyQt6.QtCore import Qsize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# =============================================================================
# def load_config(file_name):
#     config = configparser.ConfigParser()
#     config.read(file_name)
#     rf_com_port = config.get('RFGenerator', 'COMPort')
#     return rf_com_port
# 
# def main():
#     # Load the COM Port from the ini file
#     ini_file = 'hyperionTestStandControl.ini'
#     rfg_com_port = load_config(ini_file)
#     
#     resource_name = f'ASRL{rfg_com_port}::INSTR'
#     rfg = RFGenerator(resource_name)
#     
#     # Ping the VRG to see if it's talking
#     rfg.ping_device()
#     
#     # Get Frequency and power settings
#     rfg.get_frequency()
#     rfg.get_power_setting()
#     
#     # Change Frequency and Power settings
#     rfg.set_frequency(40.65)
#     rfg.set_power(800)
#     
#     # Get new frequency and power settings
#     rfg.get_frequency()
#     rfg.get_power_setting()
#     
#     
#     # close the connection
#     rfg.close()
# 
# 
# if __name__ == '__main__':
#     main()
# =============================================================================


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('VRG Control')
        button = QPushButton('Press Me!')
        
        self.setCentralWidget(button)

app = QApplication([])
window = MainWindow()
window.show()

app.exec()
    