import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use("QtAgg")

file = open('data/old-data/prop-data.csv', 'r')
rawdata = np.genfromtxt(file, delimiter=',', skip_header=2)
print(rawdata)

pwm = rawdata[:,0]
force = rawdata[:,1]
angvel = rawdata[:,2]

plt.figure(1)
plt.plot(pwm, force, 'r-', label='force(g)')
plt.xlabel('pwm')
plt.ylabel('force(g)')
plt.title('PWM vs Force')
plt.figure(2)
plt.plot(pwm, angvel, 'b-', label='Omega(Rad/s)')
plt.xlabel('pwm')
plt.ylabel('Angvel (rad/s)')
plt.title('PWM vs Angular Velocity')
plt.figure(3)
plt.plot(angvel, force, 'b-', label='Omega(Rad/s)')
plt.xlabel('angvel')
plt.ylabel('force')
plt.title('Angular Velocity vs Force')
plt.show()