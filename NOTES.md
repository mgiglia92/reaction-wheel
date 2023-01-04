Brainstorming for 1D reaction-wheel:

1. Reaction wheel has slightly unbalanced mass this way gravity field
causes a need of consistent torque from the reaction wheel. This will
cause the wheel to saturation
2. A small prop will be added to act as an "rcs thruster" and will be used
for desaturation of the wheel. 
3. The rc thruster can also be engaged during large disturbances (comobined
control system with reaction wheel and prop.


Design method and notes:
1. System should be completely housed and wireless to any external PC.
2. Allow an adjustable locatable mass to adjust the unbalance. Ideally
the reaction wheel will take 10-30 seconds to saturate that way the 
desaturation procedure isn't continuous but happens at regular intervals.
3. System will detect when reaction wheel is near saturation (maybe 60% of saturation?)
And enable a desaturation procedure. 


Electronics design:
1. uC will be either rpi pico, arduino uno (or mega), or rpi zero for wireless
comms.
2. IMU on external most part of system to detect orientation (kalman filter?)
3. Encoder will be used to get reaction wheel angular velocity and estimate
torque output. Encoder is quadrature, but either SPI or interrupt for interfacing.
4. Motor control ideally would be current control to easily generate a desired
torque. If not, voltage control (with duty cycle) will have to do and
torque estimation will have to be added.
5.

Control system design:
1. First thoughts are cascade control on angular velocity of reaction wheel.
Velocity is outer loop, and maybe current as inner loop. If not PID may be good enough.
2. System ID will be crucial in generating good gains and simulating the system.
3. RCS Thruster will be Sys ID but determining force generated for each voltage applied.
4. RCS Thruster will be On/Off control to simulate a real gas thruster.
5. Orientation control will need a disturbance rejection method implemented so
that during desaturation orientation can be held within some precision.
6. Precision of system output will be as high as possible with materials available.

CAD:
1. Need to add clamping to motor shaft.
2. Need to add mounts for arduino, motor controllers, battery.
3. Add balance adjustment
4. Add reaction wheel mass
5. Fasteners for motor mount need counter bore or counter sink


Data Collection Notes:
1. Prop pwm=60 for inertia tests, 12V on supply. Prop sees ~2.82V
	This maps to ~5.58g of thrust, applied at a radius of 68mm
	Force Applied is ~0.0547 N
	Torque applied would be ~0.00372 Nm
