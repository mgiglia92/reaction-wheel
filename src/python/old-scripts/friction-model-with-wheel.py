"""
NOTE: MPU6050 LPF set to '3' which is 42Hz bandwidth for gyroscope 4.8ms delay
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import os
import scipy.signal as signal

sos = signal.butter(N=2, Wn=10, output='sos', fs=100)

dir = path.dirname(__file__)
fname = os.path.join(dir, './data/friction-with-wheel.csv')
file = open(fname,'r')
data = np.genfromtxt(file, skip_header=1, delimiter=',')
sample = data[:,0]
ax = data[:,1]
az = data[:,3]
wy = data[:,5]
dt = data[:,7]
count = data[:,9]
count = count - count[0]

time=np.empty((len(dt)),dtype=np.float32)
for i,d in enumerate(dt):
    time[i] = np.sum(dt[0:i])

# Process data
theta = np.arctan2(ax,az)
thetadot = np.gradient(theta, time)
asat = np.gradient(wy, time)

plt.figure(0)
plt.plot(time, wy, 'r',label='sat ang vel')
plt.plot(time, asat, 'g', label='sat ang accel (friction)')
plt.legend()
plt.figure(1)
plt.plot(time, theta, 'r.', label='theta')
plt.plot(time, thetadot, 'g.', label='thetadot')
plt.legend()
plt.figure(2)
plt.plot(time, ax, 'r', label='ax')
plt.plot(time,az, 'b', label='az')
plt.legend()
plt.show()

print("DF")