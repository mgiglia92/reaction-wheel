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
fname = os.path.join(dir, './data/inertia-ratio-wheel.csv')
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

N = 51
PPR = 12
count = 360*count/(N*PPR) # convert to degrees
countfilt = signal.sosfilt(sos, count)
ww = np.gradient(count, time) # Convert to deg/sec
wwfiltpre = np.gradient(countfilt,time)
aw = np.gradient(ww, time)
awfilt = np.gradient(wwfiltpre, time)
wyfilt = signal.sosfilt(sos,wy)
asat = np.gradient(wyfilt, time)
amvavg = np.convolve(asat, [1/50]*50, mode='same')

plt.figure(0)
plt.plot(time, ww, 'r',label='none')
plt.plot(time, wwfiltpre, 'g', label='pre')
plt.plot(time, wyfilt, 'b', label='sat ang vel')
plt.title("Angular Velocities")
plt.xlabel("Time(s)")
plt.ylabel("Angvel (deg/sec)")
plt.legend()
plt.figure(1)
plt.plot(time, aw, 'r', label='alpha wheel')
plt.plot(time, awfilt, 'g', label='alpha wheel(filter)')
plt.plot(time, asat, 'b', label='alpha satellite')
plt.title("Angular Accelerations")
plt.xlabel("Time(s)")
plt.ylabel("Angacc (deg/sec2)")
plt.legend()
plt.figure(2)
plt.plot(time, amvavg, 'r', label='alpha mv avg')
plt.legend()
plt.show()

print("DF")