"""
NOTE: MPU6050 LPF set to '3' which is 42Hz bandwidth for gyroscope 4.8ms delay 
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import os
import scipy.signal as signal


Wn1 = 40
Wn2 = 10
sos = signal.butter(N=2, Wn=Wn1, output='sos', fs=100)
sos2 = signal.butter(N=2, Wn=Wn2, output='sos', fs=100)

dir = path.dirname(__file__)
fname = os.path.join(dir, './data/motor-tests/12v-step-input-test.csv')
file = open(fname,'r')
data = np.genfromtxt(file, skip_header=1, delimiter=',')
sample = data[:,0]
dt = data[:,1]
count = data[:,3]*-1 # Convert rotational direction
count = count - count[0]

time=np.empty((len(dt)),dtype=np.float32)
for i,d in enumerate(dt):
    time[i] = np.sum(dt[0:i])

N = 51
PPR = 12
count = 360*count/(N*PPR) # convert to degrees
countfilt = signal.sosfilt(sos, count)
wmotor = np.gradient(count,time)
wmotorfilt = signal.sosfilt(sos, wmotor)
amotor = np.gradient(wmotor, time)
amotorfilt = np.gradient(wmotorfilt, time)

plt.figure(0)
plt.plot(time, wmotor, 'r:', markersize=3,label=f'Ang Vel Wheel')
plt.plot(time, wmotorfilt, 'b:', label=f'Ang Vel Sat (bw={Wn1}Hz)')
# plt.plot(time, wnof, 'c', label='Omega no Fric')
plt.title("Angular Velocities in Inertial Frame")
plt.xlabel("Time(s)")
plt.ylabel("Angvel (deg/sec)")
plt.legend()
plt.figure(1)
plt.plot(time, amotor, 'r', label=f'Ang Acc Wheel')
plt.plot(time, amotorfilt, 'b', label=f'Ang Acc Wheel (bw={Wn1}Hz)')
plt.title("Angular Accelerations")
plt.xlabel("Time(s)")
plt.ylabel("Angacc (deg/sec2)")
plt.legend()
plt.show()

print("DF")