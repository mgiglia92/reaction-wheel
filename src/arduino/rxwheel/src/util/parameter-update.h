#ifndef RXWHEEL_PARAMETER_UPDATE_H
#define RXWHEEL_PARAMETER_UPDATE_H


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
    c0->setTimeParameters(comms->config0.ts, comms->config0.sigma);
    c0->setLimits(comms->config0.lowerLimit, comms->config0.upperLimit);
    c0->setDeadbands(comms->config0.deadband_radius*-1, comms->config0.deadband_radius);

    //Controller 1
    c1->setGains(comms->config1.kp, comms->config1.ki, comms->config1.kd);
    c1->setTimeParameters(comms->config1.ts, comms->config1.sigma);
    c1->setLimits(comms->config1.lowerLimit, comms->config1.upperLimit);
    c1->setDeadbands(comms->config1.deadband_radius*-1, comms->config1.deadband_radius);
    
    //Controller 2
    c2->setGains(comms->config2.kp, comms->config2.ki, comms->config2.kd);
    c2->setTimeParameters(comms->config2.ts, comms->config2.sigma);
    c2->setLimits(comms->config2.lowerLimit, comms->config2.upperLimit);
    c2->setDeadbands(comms->config2.deadband_radius*-1, comms->config2.deadband_radius);
    
    //Controller 3 
    c3->setGains(comms->config3.kp, comms->config3.ki, comms->config3.kd);
    c3->setTimeParameters(comms->config3.ts, comms->config3.sigma);
    c3->setLimits(comms->config3.lowerLimit, comms->config3.upperLimit);
    c3->setDeadbands(comms->config3.deadband_radius*-1, comms->config3.deadband_radius);
    
    //Controller 4
    c4->setGains(comms->config4.kp, comms->config4.ki, comms->config4.kd);
    c4->setTimeParameters(comms->config4.ts, comms->config4.sigma);
    c4->setLimits(comms->config4.lowerLimit, comms->config4.upperLimit);
    c4->setDeadbands(comms->config4.deadband_radius*-1, comms->config4.deadband_radius);

}

void updateValues(SerialComms *comms, CmdVals_t *vals)
{
    vals->thetaSetpoint = comms->cmdVals.thetaSetpoint;
    vals->thetaDotSetpoint = comms->cmdVals.thetaDotSetpoint;
    vals->startTest = comms->cmdVals.startTest;
    vals->runController = comms->cmdVals.runController;
}

#endif