import numpy as np

# Weight
m = 0.01615 #kg
g = 9.81

# Radius applied (m)
r = 0.095
# Torque Applied (Nm)
T = r*m*g

# Observed Acceleration
a = 456.66666*np.pi/180 #rad/sec

# Estimated total Inertia
Itot = T/a

# Observed Angular velocity ratio
asat = 4880 #deg/s2
awheel = -1432.5 #deg/s2
Iratio = -1*awheel/asat # ratio (sat/wheel)
Iwheel = Itot/(1+Iratio)
Isat = Itot - Iwheel

print(f"Itot: {Itot}\nIwheel: {Iwheel}\nIsat: {Isat}\nIratio: {Iratio}")