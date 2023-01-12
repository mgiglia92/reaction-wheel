"""
NOTE: MPU6050 LPF set to '3' which is 42Hz bandwidth for gyroscope 4.8ms delay 
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import os
import scipy.signal as signal

Torque = 0.0547 * 68 #Newtons*mm

Wn = 10
sos = signal.butter(N=1, Wn=Wn, output='sos', fs=100, analog=False)

dir = path.dirname(__file__)
fname = os.path.join(dir, './data/weight-tests/vertical2.csv')
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

N = 51
PPR = 12
count = 360*count/(N*PPR) # convert to degrees
countfilt = signal.sosfiltfilt(sos, count)
ww = np.gradient(count, time) # Convert to deg/sec
wwfiltpre = np.gradient(countfilt,time)
aw = np.gradient(ww, time)
awfilt = np.gradient(wwfiltpre, time)
wsatfilt = signal.sosfiltfilt(sos,wsat)
asat = np.gradient(wsat, time)
asatfilt = np.gradient(wsatfilt, time)

# Add theoretical friction acceleration to sattelite motion data
B = -200
#integrate acceleration with frictino removed
wnof = np.empty((len(asat)), dtype=np.float32)
for i,w in enumerate(wsat):
        wnof[i] = wsat[i] + B*time[i]
anof = np.gradient(wnof, time)
jfilt = np.gradient(asatfilt,time)
# separator = np.where(abs(jfilt)>5000)
sep1 = signal.find_peaks(jfilt, 5000)
sep2 = signal.find_peaks(-1*jfilt, 5000)

plt.figure(0)
plt.plot(time, wsat, 'r', label='sat ang vel')
plt.plot(time, wsatfilt, 'b', label=f'sat ang vel (filtered, bw={Wn}Hz)')
plt.plot(time, wnof, 'g', label='sat ang vel (no fric)')
for s,d in zip(sep1[0],sep2[0]):
    plt.axvline(time[s], color='black', linestyle=':')
    plt.axvline(time[d], color='black', linestyle=':')
plt.title("Angular Velocities")
plt.xlabel("Time(s)")
plt.ylabel("Angvel (deg/sec)")
plt.legend()

plt.figure(1)
plt.title("Angular Acceleration")
plt.xlabel("Time (s)")
plt.ylabel("Angular Acceleration (deg/s2)")
plt.plot(time, asat, 'r', label='ang acc')
plt.plot(time, asatfilt, 'b', label=f'ang acc (filtered, bw={Wn}Hz)')
plt.plot(time, anof, 'g', label='ang acc (no fric)')
for s,d in zip(sep1[0],sep2[0]):
    plt.axvline(time[s], color='black', linestyle=':')
    plt.axvline(time[d], color='cyan', linestyle=':')
plt.legend()
plt.figure(2)
plt.title("Friction vs. Angular Vel")
plt.xlabel("Angular Velocity (deg/sec)")
plt.ylabel("Friction Acceleration")
plt.plot(wsat[sep1[0][0]:sep1[0][1]], asat[sep1[0][0]:sep1[0][1]], 'r', label='Friction Acceleration')
plt.show()

print("DF")