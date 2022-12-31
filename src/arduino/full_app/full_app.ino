#include <rxwheel.h>

SerialComms comms;
MPU6050 imu;
PID_control c0, c1, c2, c3, c4;

unsigned long cur, prev;
unsigned long dt = 10000;
int counter = 0;
bool flip = false;
int power=0;

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  imu.begin();
  motorSetup();
}

void loop() {
  cur = micros();

  comms.handleCommand();
  if (cur - prev > dt) {
    imu.update();
    if(comms.start)
    {
      power = 255;
    }
    else{ power = 0; }

    comms.sendData((cur - prev) / 1000000.0, imu.getAccelX(), imu.getAccelZ(), imu.getAngVelY(), power);
    prev = cur;
  }

  //Write motor power and direction
  rawMotorCtrl(0, -1 * power);
  
  //Check if comms have param changes, update all values
  if (comms.updateParams)
  {
    updateIMU(&comms, &imu);
    updateControllers(&comms, &c0, &c1, &c2, &c3, &c4);
    comms.updateParams = false;
  }
}
