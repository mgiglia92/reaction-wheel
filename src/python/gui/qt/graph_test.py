from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from util.serial_comms import ArduinoComms
from gui.qt.ui import Ui_MainWindow
import io
from ruamel.yaml import YAML
yaml = YAML()
from threading import Thread
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog

class Ui_MainWindowFull(Ui_MainWindow):
    def setup(self):
        self.connectButton.clicked.connect(lambda: self.arduinoConnect(self.deviceName.text()))
        self.yamlFileLocationButton.clicked.connect(self.yamlFileDialog)
        self.dataFileLocationButton.clicked.connect(self.dataFileDialog)
        self.comms = ArduinoComms()
        self.loadYamlButton.clicked.connect(self.loadYaml)
        self.saveYamlButton.clicked.connect(self.saveYaml)
        self.timer = QTimer(self)

    def yamlFileDialog(self):
        options = QFileDialog.Options()
        directoryName= QFileDialog.getExistingDirectory(self, "Choose YAML Location")
        self.yamlLocationLabel.setText(directoryName)

    def dataFileDialog(self):
        options = QFileDialog.Options()
        directoryName= QFileDialog.getExistingDirectory(self, "Choose Data Location")
        self.dataLocationLabel.setText(directoryName)

    def plotfunc(self):
        try:
            # Process all the data in the queue
            while not self.comms.dataQueue.empty():
                self.comms.data.append(self.comms.processDataMessage(self.comms.dataQueue.get()))
            # Clear graphs and plot the last 500 data points
            self.graphWidget.clear()
            self.graphWidget_2.clear()
            self.graphWidget.plot(self.comms.data.ax[-500:-1])
            self.graphWidget_2.plot(self.comms.data.wy[-500:-1])
        except:
            pass
        self.timer.start(100)


    def arduinoConnect(self, port):
        self.comms.connect(port)
        self.timer.timeout.connect(self.plotfunc)
        self.timer.start(100)
    
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
        self.yamlEditor.append(buf.getvalue()) # Put the yaml text
        file.close()
    
    def saveYaml(self):
        text = self.yamlEditor.toPlainText() # Get text for update yaml file
        file = open(os.getcwd()+'/src/python/yaml/' + self.saveYamlFileName.text(), 'wb') # get the filename
        file.write(bytes(text, 'utf-8'))# Write to the file
        file.close()# Close the file 
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindowFull):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setObjectName("Reaction Wheel GUI")
        self.setup()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()