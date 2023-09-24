"""
NOTE: MPU6050 LPF set to '3' which is 42Hz bandwidth for gyroscope 4.8ms delay 
"""

import numpy as np
import matplotlib.pyplot as plt
from os import path
import os
import scipy.signal as signal


Wn1 = 5
Wn2 = 1
sos = signal.butter(N=1, Wn=Wn1, output='sos', fs=100)
sos2 = signal.butter(N=1, Wn=Wn2, output='sos', fs=100)

dir = path.dirname(__file__)
fname = os.path.join(dir, './data/inertia-ratio-tests/vertical-inertia-test2.csv')
file = open(fname,'r')
data = np.genfromtxt(file, skip_header=1, delimiter=',')
sample = data[:,0]
ax = data[:,1]
az = data[:,3]
wsat = data[:,5]
dt = data[:,7]
count = data[:,9]*-1 # Convert rotational direction
count = count - count[0]

time=np.empty((len(dt)),dtype=np.float32)
for i,d in enumerate(dt):
    time[i] = np.sum(dt[0:i])

N = 51
PPR = 12
count = 360*count/(N*PPR) # convert to degrees
countfilt = signal.sosfiltfilt(sos, count)
wsatfilt = signal.sosfiltfilt(sos, wsat)
wws = np.gradient(count, time) # Wheel rot rate in satellite frame
wwsfilt = signal.sosfiltfilt(sos,wws)
aw = np.gradient(wws, time) # Acceleration of wheel in sat frame
wwe = wws + wsat  # Get angular vel of wheel in inertial frame
wwefilt = wwsfilt + wsatfilt
# Add theoretical friction acceleration to sattelite motion data
B = 200
#integrate acceleration with frictino removed
wsatnof = np.zeros((len(aw)), dtype=np.float32)
wsatnof[0] = wsat[0]
# Predict motion of system if friction was removed
for i,w in enumerate(wsat):
        if i == len(wsat)-1: break
        wsatnof[i+1] = wsat[i] + B*time[i]


wwenof = wws + wsatnof  # Get angular vel of wheel in inertial frame
# Angular Accelerations
awe = np.gradient(wwe,time)
awefilt = np.gradient(wwefilt,time)
asat = np.gradient(wsat, time)
asatfilt = np.gradient(wsatfilt,time)
awenof = np.gradient(wwenof, time) # Wheel ang acc in inertial frame
asatnof = np.gradient(wsatnof, time) # Sat ang acc with no friction
    

plt.figure(0)
plt.plot(time, wwefilt, 'r:', markersize=3,label=f'Ang Vel Wheel (Inertial Frame, lpf bw={Wn1}Hz)')
plt.plot(time, wsatfilt, 'b:', label=f'Ang Vel Sat (Inertial Frame, lpf bw={Wn1}Hz)')
plt.plot(time, wwenof, 'r',label=f'Ang Vel Wheel (Inertial Frame, no fric)')
plt.plot(time, wsatnof, 'b', label=f'Ang Vel Sat (Inertial Frame, no fric)')
# plt.plot(time, wnof, 'c', label='Omega no Fric')
plt.title("Angular Velocities in Inertial Frame")
plt.xlabel("Time(s)")
plt.ylabel("Angvel (deg/sec)")
plt.legend()
plt.figure(1)
plt.plot(time, awefilt, 'r', label=f'Ang Acc Wheel (Inertial Frame, bw={Wn1}Hz)')
plt.plot(time, asatfilt, 'b', label=f'Ang Acc Sat (Inertial Frame,  bw={Wn1}Hz)')
plt.title("Angular Accelerations")
plt.xlabel("Time(s)")
plt.ylabel("Angacc (deg/sec2)")
plt.legend()
plt.show()


print("DF")