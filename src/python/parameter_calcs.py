import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

g = 9.81 #m/s2

Irx = 53.8 # Moment of inertia of reaction mass (not including motor) kg mm2
Imotor = 10
Ibody = 221.3 # I of the "satelite" minus reaction mass

wmax = 187*2*np.pi/60 # Max angular velocity of motor
ratio = 1/51 # Gear ratio of motor to output

L_max = Irx*wmax + (Imotor*(wmax/ratio))

# Given a small unbalanced mass of the satellite, determine the amount of time it would take to saturate the wheel
# Assume the unbalanced mass is at an angle that gravity causes the most torque
m_unbal = 10 # g
r_unbal = 0.1 # m
T_unbal = m_unbal * g * r_unbal

t_saturate = L_max / T_unbal


print(t_saturate)
