import numpy as np
import csv

class DataFormat:
    def __init__(self):
        pass
        self.time               = np.empty((0),dtype=np.float32)
        self.theta_desired      = np.empty((0),dtype=np.float32)
        self.theta_actual       = np.empty((0),dtype=np.float32)
        self.omega_actual_sat   = np.empty((0),dtype=np.float32)
        self.omega_actual_wheel = np.empty((0), dtype=np.float32)
        self.index=0
    def append(self, data):
        if(len(self.time) >= 10000):
            self.__init__()
        self.time               = np.append(self.time, data[0])
        self.theta_desired      = np.append(self.theta_desired, data[1])
        self.theta_actual       = np.append(self.theta_actual, data[2])
        self.omega_actual_sat   = np.append(self.omega_actual_sat, data[3])
        self.omega_actual_wheel = np.append(self.omega_actual_wheel, data[4])
    def tocsv(self):
        pass