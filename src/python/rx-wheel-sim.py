import numpy as np
import matplotlib.pyplot as plt
from util.control_util import PID

class Wheel:
    def __init__(self, pid: PID):
        self.Iwheel = 1.2 #kgmm2
        self.wmax = 10 #rad/sec
        self.ctrl = pid
        self.state = np.array([0,0]).reshape((2,1)) # [Theta, Omega]
        self.k = 1.1
        self.R = 0.6

    def step(self, torque):
        # Get angular vel required to generated desired torque I*delta(Omega)
        wdes = (torque/self.Iwheel) + self.state[1]
        wprev = self.state[1]
        self.state = self.state + self.xdot(self.ctrl.step(wdes, self.state[1]))*self.ctrl.dt
        self.last_torque = self.state[1] - wprev
        # self.state = self.state + self.xdot(10)*self.ctrl.dt

    def xdot(self, v):
        # Determine torque applied to motor from voltage applied
        u = ((v-(self.state[1]*self.k))/self.R)*self.k

        return np.array([self.state[1], u/self.Iwheel])
    
class Sat:
    def __init__(self, wheel, ctrl: PID):
        self.I = 20
        self.state = np.array([0,0]).reshape((2,1))
        self.ctrl = ctrl
        self.wheel = wheel
    
    def step(self, desired):
        # Determine desired counter torque
        torque = self.ctrl.step(desired, self.state[0])
        # Pass desired torque into wheeel
        self.wheel.step(torque)
        # Respect conservation of angular momentum
        self.state[1] = (self.wheel.Iwheel*self.wheel.state[1])/self.I
        # Project state 1 time step into future
        self.state = self.state + np.array([self.state[1], self.wheel.last_torque])*self.ctrl.dt

class StateHistory:
    def __init__(self):
        self.state = np.zeros((2,1))
        self.time = np.zeros((1))
    
    def append(self, t, s):
        self.state = np.concatenate((self.state, s), axis=1)
        self.time = np.concatenate((self.time, t), axis=0)

if __name__ == "__main__":
    pid = PID(0.01, -9, 9, 10, 0, 0.01, True)
    pid2 = PID(0.01, -100, 100, 1, 0, 0.1, True)
    w = Wheel(pid)
    sat = Sat(w, pid2)
    N = 300
    hist = StateHistory()
    wheelhist = StateHistory()

    for i in range(N):
        sat.step(1)
        hist.append(np.array([i*sat.ctrl.dt]), sat.state)
        wheelhist.append(np.array([i*sat.ctrl.dt]), sat.wheel.state)
    
    fig,ax = plt.subplots(2,2)
    ax[0,0].plot(hist.time, hist.state[0,:])
    ax[0,0].set_ylabel('Sat Theta (rad)')
    ax[1,0].plot(hist.time, hist.state[1,:])
    ax[1,0].set_ylabel('Sat Omega (rad/sec)')
    ax[1,0].set_xlabel('Time (s)')
    ax[0,1].plot(hist.time, wheelhist.state[0,:])
    ax[0,1].set_ylabel('Wheel Theta (rad/sec)')
    ax[1,1].plot(hist.time, wheelhist.state[1,:])
    ax[1,1].set_ylabel('Wheel Omega (rad/sec)')
    plt.show(block=True)
    print("N")