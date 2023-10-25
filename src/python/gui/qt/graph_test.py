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
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog
from util.data_util import DataFormat
from util.parameters_util import ParameterConverter
import traceback
import numpy as np
from time import time_ns, sleep

class Ui_MainWindowFull(Ui_MainWindow):
    def setup(self):
        self.connectButton.clicked.connect(lambda: self.arduinoConnect(self.deviceName.text()))
        self.disconnectButton.clicked.connect(self.arduinoDisconnect)
        self.yamlFileLocationButton.clicked.connect(self.yamlFileDialog)
        self.dataFileLocationButton.clicked.connect(self.dataFileDialog)
        self.comms = ArduinoComms()
        self.loadYamlButton.clicked.connect(self.loadYaml)
        self.saveYamlButton.clicked.connect(self.saveYaml)
        self.startCommsButton.clicked.connect(self.startComms)
        self.startControllerButton.clicked.connect(self.startController)
        self.stopCommsButton.clicked.connect(self.stopComms)
        self.clearDataButton.clicked.connect(self.clearData)
        self.pushParamsButton.clicked.connect(self.pushParams)
        self.sendSetPointButton.clicked.connect(self.pushSetpoint)
        self.timer = QTimer(self)
        # Set graph Button IDs
        self.plotSelector1ButtonGroup.setId(self.plotA, 1)
        self.plotSelector1ButtonGroup.setId(self.plotB, 2)
        self.plotSelector1ButtonGroup.setId(self.plotC, 3)
        self.plotSelector1ButtonGroup.setId(self.plotD, 4)
        self.plotSelector1ButtonGroup.setId(self.plotE, 5)
        self.plotSelector2ButtonGroup.setId(self.plotA_2, 1)
        self.plotSelector2ButtonGroup.setId(self.plotB_2, 2)
        self.plotSelector2ButtonGroup.setId(self.plotC_2, 3)
        self.plotSelector2ButtonGroup.setId(self.plotD_2, 4)
        self.plotSelector2ButtonGroup.setId(self.plotE_2, 5)
        self.plot1 = [False]*5
        self.plot2 = [False]*5
        #TODO: Make a damn plotting library already dude
        # Plot colors (I know why they here bro)
        red     = pg.mkPen(pg.hsvColor(hue=0.0,   sat=0.8,      val=0.8,      alpha=0.5), width=2)
        blue    = pg.mkPen(pg.hsvColor(hue=0.2,   sat=0.8,      val=0.8,      alpha=0.5), width=2)
        green   = pg.mkPen(pg.hsvColor(hue=0.4,   sat=0.8,      val=0.8,      alpha=0.5), width=2)
        color4  = pg.mkPen(pg.hsvColor(hue=0.6,   sat=0.8,      val=0.8,      alpha=0.5), width=2)
        color5  = pg.mkPen(pg.hsvColor(hue=0.8,   sat=0.8,      val=0.8,      alpha=0.5), width=2)
        self.colors=[red, green, blue, color4, color5]

        # AUto set point for showcase
        self.setPointTimer = QTimer(self)
        self.setPointTimer.timeout.connect(self.autoSetPoint)

    def clearData(self):
        self.comms.data = DataFormat()

    def startComms(self):
        self.comms.sendMessage("$R1%")

    def startController(self):
        self.comms.sendMessage("$R2%")

    def stopComms(self):
        self.comms.sendMessage("$R0%")
    
    def pushSetpoint(self):
        # TODO: Add a button to do this, uncomment the pushing setpoint
        # Toggle auto setpoint sender
        self.setPointTimer.start(100)

        # val = self.setPointDoubleSpinBox.value()
        # self.comms.sendMessage(f"$S0,A{val}%")

    def autoSetPoint(self):
        val = np.sin(2*np.pi*0.2*float(time_ns()/1000000000.0))
        self.comms.sendMessage(f"$S0,A{val:.2f}%")
        self.setPointTimer.start(20)

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
            #clear plots
            self.graphWidget.clear()
            self.graphWidget_2.clear()

            maxpoints = self.numDataPointsSpinBox.value()
            startpoint = self.startDataPointSpinBox.value()
            length = len(self.comms.data.time)
            numpoints = min(maxpoints, length-startpoint)

            # Check what to plot
            for i,b in enumerate(self.plotSelector1ButtonGroup.buttons()):
                self.plot1[i] = b.isChecked()
            for i,b in enumerate(self.plotSelector2ButtonGroup.buttons()):
                self.plot2[i] = b.isChecked()

            self.graphWidget.addLegend()
            if self.plot1[0]: 
                self.graphWidget.plot(self.comms.data.time[-1*numpoints:-1],                pen=self.colors[0],     name="Ts")
            if self.plot1[1]:
                self.graphWidget.plot(self.comms.data.theta_desired[-1*numpoints:-1],       pen=self.colors[1],     name="Theta Desired")
            if self.plot1[2]:
                self.graphWidget.plot(self.comms.data.theta_actual[-1*numpoints:-1],        pen=self.colors[2],     name="Theta Actual")
            if self.plot1[3]:
                self.graphWidget.plot(self.comms.data.omega_actual_sat[-1*numpoints:-1],    pen=self.colors[3],     name="Omega_Actual_Satellite")
            if self.plot1[4]:
                self.graphWidget.plot(self.comms.data.omega_actual_wheel[-1*numpoints:-1],  pen=self.colors[4],     name="Omega_Actual_RxWheel")            

            self.graphWidget.addLegend()
            if self.plot2[1]:
                self.graphWidget_2.plot(self.comms.data.time[-1*numpoints:-1],                  pen=self.colors[0],     name="Ts")
            if self.plot2[2]:
              self.graphWidget_2.plot(self.comms.data.theta_desired[-1*numpoints:-1],           pen=self.colors[1],     name="Theta Desired")
            if self.plot2[4]:
              self.graphWidget_2.plot(self.comms.data.theta_actual[-1*numpoints:-1],            pen=self.colors[2],     name="Theta Actual")
            if self.plot2[0]:
              self.graphWidget_2.plot(self.comms.data.omega_actual_sat[-1*numpoints:-1],        pen=self.colors[3],     name="Omega_Actual_Satellite")
            if self.plot2[3]:
                self.graphWidget_2.plot(self.comms.data.omega_actual_wheel[-1*numpoints:-1],    pen=self.colors[4],     name="Omega_Actual_RxWheel")
            
        except:
            pass
        self.timer.start(20)


    def arduinoConnect(self, port):
        self.comms.connect(port)
        self.timer.timeout.connect(self.plotfunc)
        self.timer.start(100)

    def arduinoDisconnect(self):
        print('trying to disconnect')
        try:
            self.comms.close()
            self.comms.killProcess = True
            print("sucessfully disconnected")
        except Exception as e:
            print(e)

    def loadYaml(self):
        filename = self.loadYamlFileName.text()
        try:
            file = open(self.yamlLocationLabel.text() + '/' + filename)
        except:
            print("Invalid file")
            return False
       
        params = yaml.load(file) #Get params yaml file
        buf = io.StringIO() #Get StringIO buffer
        yaml.dump(params, buf) # Dump the yaml file into the StringIO buffer
        self.yamlEditor.clear() # Clear all text from the editor
        self.yamlEditor.append(buf.getvalue()) # Put the yaml text
        file.close()
    
    def saveYaml(self):
        text = self.yamlEditor.toPlainText() # Get text for update yaml file
        file = open(self.yamlLocationLabel.text() + '/' + self.saveYamlFileName.text(), 'wb') # get the filename
        file.write(bytes(text, 'utf-8'))# Write to the file
        file.close()# Close the file 

    def pushParams(self):
        p = ParameterConverter(self.yamlLocationLabel.text() + '/' +self.loadYamlFileName.text())
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindowFull):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setObjectName("Reaction Wheel GUI")
        self.setup()

def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
    except:
        traceback.print_exception()
    main = MainWindow()
    main.show()
    ret = app.exec_()
    sys.exit(ret)

if __name__ == '__main__':
    main()