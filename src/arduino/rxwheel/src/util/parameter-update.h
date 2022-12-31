#ifndef RXWHEEL_H
#define RXWHEEL_H


#include "sensor/mpu6050.h"
#include "sensor/odom.h"
#include "util/array.h"
#include "util/differentiator.h"
#include "util/pid-control.h"
#include "util/SerialComms.h"
#include "util/parameter-update.h"


#endif /* RXWHEEL_H */

void updateIMU(SerialComms *comms, MPU6050 *imu)
{
	// set LPF settings
	imu->wire->beginTransmission(imu->i2c_addr);
	imu->wire->write(0x1a);
	imu->wire->write(comms->LPF);
	imu->wire->endTransmission();
}

void updateControllers(SerialComms *comms, PID_control *c0, PID_control *c1, PID_control *c2, PID_control *c3, PID_control *c4)
{
    //Controller 0
    c0->setGains(comms->config0.kp, comms->config0.ki, comms->config0.kd);

    //Controller 1
    c1->setGains(comms->config1.kp, comms->config1.ki, comms->config1.kd);

    //Controller 2
    c2->setGains(comms->config2.kp, comms->config2.ki, comms->config2.kd);

    //Controller 3 
    c3->setGains(comms->config3.kp, comms->config3.ki, comms->config3.kd);

    //Controller 4
    c4->setGains(comms->config4.kp, comms->config4.ki, comms->config4.kd);

}