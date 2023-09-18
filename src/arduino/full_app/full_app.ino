#include <rxwheel.h>

float controllerbandwidth = 40; //Hz
float omegaBandwidth = 40;
float alphaBandwidth = 1;
float Iwheel = 0.0019098;
float Isat = 0.00042853;

SerialComms comms;
CmdVals_t cmdVals{0, 0, 0, 0, 0};
MPU6050 imu;
PID_control c0, c1, c2, c3, c4;
Differentiator wheeldiff(0.01, 1 / (omegaBandwidth * 2 * PI));
Differentiator acceldiff(0.01, 1 / (alphaBandwidth * 2 * PI));

unsigned long cur, prev;
unsigned long dt = 10000;
int counter = 0;
bool flip = false;
float power, thrusterPower;
int pwm, thrusterPwm;
int32_t count = 0;
float N = 51;
float wwheelDesired, wwheelActual, torqueDesired, wSat, wSatDesired, thetaSat, awheel;

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  imu.begin();
  imu.calibrate();
  motorSetup();
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), doA, RISING);

  //default c0 for a moment (motor vel)
  c0.setGains(0.824674, 9.132689, -0.000339689);
  c0.setTimeParameters(0.01, 1 / (controllerbandwidth * 2 * PI));
  c0.setLimits(-12, 12);
  c0.setDeadbands(-2, 2);
  c0.antiWindupEnabled = true;
  //Sat Omega controller (inner loop)
  c1.setGains(0.005, 0.00001, 0);
  c1.setTimeParameters(0.01, 1 / (controllerbandwidth * 2 * PI));
  c1.setLimits(-15, 15);
  c1.antiWindupEnabled = true;
  //  c1.setDeadbands(-3.6, 3.6);
  //Sat Theta controller (outer loop)
  c2.setGains(10, 0, 0);
  c2.setTimeParameters(0.01, 1 / (controllerbandwidth * 2 * PI));
  c2.setLimits(-3.14, 3.14);
  c2.antiWindupEnabled = true;
  //motor acceleration control
  c3.setGains(0.1, 0.4, 0);
  c3.setTimeParameters(0.01, 1 / (controllerbandwidth * 2 * PI));
  c3.setLimits(-12, 12);
  c3.antiWindupEnabled = true;
  c3.setDeadbands(-2, 2);
}

void loop() {
  cur = micros();

  comms.handleCommand();
  if (cur - prev > dt) {
    imu.update();
    if (cmdVals.startTest && !cmdVals.runController)
    {
      power = 12;
    }
    //Run feedback control
    else if (cmdVals.runController && !cmdVals.startTest)
    {
      wSat = imu.getAngVelY() * PI / 180;
      //Estimate motor velocity (in sat frame, rad/sec)
      wwheelActual = wheeldiff.differentiate(2 * PI * count / (12 * N));
      awheel = acceldiff.differentiate(wwheelActual);

      thetaSat = thetaSat + wSat * (dt / 1000000.0); // Integrate wSat to get theta (approximate

      // Outer loop of sat (sat theta)
      wSatDesired = c2.pid(cmdVals.thetaSetpoint, thetaSat);
      //        wSatDesired = 1.5;

      //Inner Loop of Sat (sat ang vel)
      torqueDesired = c1.pid(wSatDesired, wSat);
      wwheelDesired = (wwheelActual + (torqueDesired / Iwheel));
      wwheelDesired = constrain(wwheelDesired, -29, 29);
      //            wwheelDesired = 6.28;

      //Motor Velocity feedback control (using c0)
      power = c0.pid(wwheelDesired, wwheelActual);
      //Motor Acceleration control
      //      power = c3.pid(0.5, awheel);
      //Thruster ON/OFF control
      if (wwheelActual > 13) {
        thrusterPower = 3;
      }
      else if (wwheelActual < 5 && wwheelActual > -5) {
        thrusterPower = 0;
      }
      else if (wwheelActual < -13 && wwheelActual < 0) {
        thrusterPower = -3;
      }
    }
    else {
      power = 0;
      thrusterPower = 0;
      //Reset the controllers
      c0.setpointReset(0, 0);
      c1.setpointReset(0, 0);
    }

            comms.sendData((cur - prev) / 1000000.0, cmdVals.thetaSetpoint, thetaSat, imu.getAngVelY(), count);
//    comms.sendData((cur - prev) / 1000000.0, cmdVals.thetaSetpoint, cmdVals.runController, cmdVals.startTest, cmdVals.thetaDotSetpoint);

    prev = cur;
  }

  //Write motor power and direction (convert from voltage to pwm)
  pwm = int(-1 * power * 255 / 12.0);
  thrusterPwm = int(thrusterPower * 255 / 12);
  rawMotorCtrl(thrusterPwm, constrain(pwm, -255, 255));

  //Write prop power
  //  rawMotorCtrl(power, 0);

  //Check if comms have param changes, update all values
  if (comms.updateParams)
  {
    updateIMU(&comms, &imu);
    updateValues(&comms, &cmdVals);
    comms.updateParams = false;
  }
  if (comms.updateController)
  {
    updateControllers(&comms, &c0, &c1, &c2, &c3, &c4);

  }
}

void doA()
{
  int B = digitalRead(3);
  if (B == HIGH) {
    count++;
  }
  else {
    count--;
  }
}
