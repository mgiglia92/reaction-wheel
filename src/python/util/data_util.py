import numpy as np
import csv

class DataFormat:
    def __init__(self):
        pass
        self.time = np.empty((1),dtype=np.float32)
        self.ax = np.empty((1),dtype=np.float32)
        self.az = np.empty((1),dtype=np.float32)
        self.wy = np.empty((1),dtype=np.float32)
        self.index=0
    def append(self, data):
        self.time = np.append(self.time, data[0])
        self.ax = np.append(self.ax, data[1])
        self.az = np.append(self.az, data[2])
        self.wy = np.append(self.wy, data[3])
    def tocsv(self):
        pass