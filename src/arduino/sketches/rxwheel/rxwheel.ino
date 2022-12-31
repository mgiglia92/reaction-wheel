#include <rcc.h>
#include <Filter.h>

Filter f;
PID_control_config_t velconfig{
  kp: 20,
  ki: 0,
  kd: 0,
lowerLimit: -255,
  upperLimit: 255,
  sigma: 0.1,
  ts: 0.01,
errorDotEnabled: true,
antiWindupEnabled: true
};

PID_control_config_t satconfig{
  kp: 0,
  ki: 20,
  kd: 0.00001,
  lowerLimit: -5,
  upperLimit: 5,
  sigma: 0.1,
  ts: 0.01,
errorDotEnabled: true,
antiWindupEnabled: true
};

MPU6050 imu;
PID_control velcontrol(velconfig);
PID_control satcontrol(satconfig);
Differentiator diff(0.1, velconfig.ts);

//Timing variables
unsigned long cur, prev;
unsigned long dt = (int)velconfig.ts * 1000000; //in us

//State vars
double theta = 0;
double thetaprev = 0;
double desired_torque;

//Motor vars
double N = 51; //input:output ratio of motor
double count, countprev;
double motorvel;
double desired_motorvel;

//Input vars
double motorpwr;

//Sensor vars
double ax, az, wy;

void setup()
{
  Filter_init(&f);
  Serial.begin(115200);
  imu.begin();
//    imu.calibrate();
  //Set deadband outputs of motor
  velcontrol.setDeadbands(-70, 70);
  attachInterrupt(digitalPinToInterrupt(2), doA, RISING);

}

void loop()
{
  cur = micros();
  if (cur - prev >= dt)
  {
    //Get data from sensors
    calculateAngle();

    //Do sat porition feedback control
    desired_motorvel = -1 * satcontrol.pid(0, wy*(2*PI/180.0));
//    desired_motorvel = -1 * satcontrol.pid(3.14, theta);
    //Estimate motor angular velocity
    motorvel = diff.differentiate(count) / N;

    //Do Motor Velocity Feedback control
    motorpwr = velcontrol.pid(desired_motorvel, motorvel);

    //Print data
    Serial.print(motorvel);
    Serial.print(',');
    Serial.print(theta);
    Serial.print(',');
    Serial.println(desired_motorvel);

    //Reset timing variables
    prev = cur;
  }
  rawMotorCtrl(0, -1 * motorpwr);
}

double calculateAngle()
{
  thetaprev = theta;
  //Get IMU readings
  imu.update();
  //  static double ay;
  ax = imu.getAccelX();
  //  static double az;
  az = imu.getAccelZ();
  //  static double wx;
  wy = -1*imu.getAngVelY();
  //  static double norm;
  //  norm = sqrt(pow(ay,2)+pow(az,2));

  //Simple angle calc
  theta = atan2(ax, az);
//  Filter_put(&f, wy);
//  wy = Filter_get(&f);
  if (theta < 0)
  {
    theta += 2 * PI;
  }
  
//
//  //Complementary filter
//  theta = 0.9 * theta + 0.1 * (thetaprev + wy*(2*PI/180.0) * dt);

  //Output
  return theta;
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
