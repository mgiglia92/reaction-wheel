"""
NOTE: MPU6050 LPF set to '3' which is 42Hz bandwidth for gyroscope 4.8ms delay 
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import os
import scipy.signal as signal

Torque = 0.0547 * 68 #Newtons*mm

Wn = 1
sos = signal.butter(N=1, Wn=Wn, output='sos', fs=100, analog=False)

dir = path.dirname(__file__)
fname = os.path.join(dir, './data/friction-tests/vertical-friction-1.csv')
file = open(fname,'r')
data = np.genfromtxt(file, skip_header=1, delimiter=',')
sample = data[:,0]
ax = data[:,1]
az = data[:,3]
wsat = data[:,5]
dt = data[:,7]
count = data[:,9]
count = count - count[0]

time=np.empty((len(dt)),dtype=np.float32)
for i,d in enumerate(dt):
    time[i] = np.sum(dt[0:i])

wsatfilt = signal.sosfiltfilt(sos, wsat)
asat = np.gradient(wsat, time, edge_order=2)
asatfilt = signal.sosfiltfilt(sos, asat)


plt.figure(0)
plt.plot(time, wsat, 'r', label='sat ang vel')
# plt.plot(time, wsatfilt, 'b', label=f'sat ang vel (filtered, bw={Wn}Hz)')
plt.xlabel("Time(s)")
plt.ylabel("Angvel (deg/sec)")
plt.legend()

plt.figure(1)
plt.title("Angular Acceleration")
plt.xlabel("Time (s)")
plt.ylabel("Angular Acceleration (deg/s2)")
plt.plot(time, asat, 'r', label='ang acc')
plt.plot(time, asatfilt, 'b', label=f'ang acc (filtered, bw={Wn}Hz)')
plt.legend()
plt.figure(2)
plt.plot(wsat,asatfilt,'r-', label=f'accel vs omega (filtered, bw={Wn}Hz')
plt.show()


print("DF")