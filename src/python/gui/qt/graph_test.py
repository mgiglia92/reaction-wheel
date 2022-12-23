from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from util.serial_comms import ArduinoComms
from gui.qt.graph import Ui_MainWindow
import io
from ruamel.yaml import YAML
yaml = YAML()

class Ui_MainWindowFull(Ui_MainWindow):
    def setup(self):
        self.connectButton.clicked.connect(lambda: self.arduinoConnect(self.deviceName.text()))
        self.comms = ArduinoComms()
        self.loadYamlButton.clicked.connect(self.loadYaml)
        self.saveYamlButton.clicked.connect(self.saveYaml)

    def arduinoConnect(self, port):
        self.comms.connect(port)
    
    def loadYaml(self):
        filename = self.loadYamlFileName.text()
        try:
            file = open(filename)
        except:
            filename = os.getcwd() + '/src/python/yaml/' + filename
            file = open(filename)
       
        params = yaml.load(file) #Get params yaml file
        buf = io.StringIO() #Get StringIO buffer
        yaml.dump(params, buf) # Dump the yaml file into the StringIO buffer
        self.yamlEditor.clear() # Clear all text from the editor
        self.yamlEditor.appendPlainText(buf.getvalue()) # Put the yaml text
    
    def saveYaml(self):
        pass
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindowFull):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()