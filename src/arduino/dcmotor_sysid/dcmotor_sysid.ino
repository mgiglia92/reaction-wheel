#define DIRA 12
#define DIRB 13
#define PWMA 3
#define PWMB 11
#define ENCA 18
#define ENCB 19
#define ratio 51.0

unsigned long cur, prev, t0, t1;
unsigned long dt = 50000;
uint16_t power = 10;

// State machine vars
int state = 0;

//Ang vel vars
volatile int count = 0;
int countprev = 0;
double wavg;
int index;

void setup() {
  Serial.begin(115200);
  pinMode(DIRA, OUTPUT);
  pinMode(DIRB, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(ENCA, INPUT_PULLUP);
  pinMode(ENCB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCA), doA, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB), doB, CHANGE);
  digitalWrite(DIRA, HIGH);
  //  analogWrite(PWMA, 100);
  //  while (true) {
  //    Serial.println(count);
  //  }
}

void loop() {
  cur = micros();
  //  Serial.println(count);
  switch (state)
  {
    case 0: //Set motor power
      analogWrite(PWMA, power);
      state = 1;
      break;

    case 1: //Print to serial monitor go to state 2
      Serial.print("PWM: ");
      Serial.println(power);
      t0 = micros();
      state = 2;
      Serial.println("Prop stabilizing");
      break;

    case 2: //Let prop stabilize to ang vel for 0.25s
      if ((cur - t0) >= 250000) {
        state = 3;
        t0 = micros();
        t1 = micros();
        Serial.print("ANG VEL: ");
        noInterrupts();
        countprev = count;
        interrupts();
        index = 0;
        wavg = 0;
      }
      break;

    case 3:
      if ((cur - t0) >= 3000000) {
        state = 0;
        power += 10;
        if (power > 255) {
          power = 255;
        } Serial.println();
      }
      if ((cur - t1) >= 500000) {
        noInterrupts();
        double w = calc_omega((count - countprev), (cur - t1) / 1000000.0);
        countprev = count;
        interrupts();
        Serial.print(" | "); Serial.print();
        noInterrupts();
        countprev = count;
        interrupts();
        t1 = cur;
      }
      break;

  }

}

double calc_omega(double dcount, double dt)
{
  return dcount / (dt * ratio);
}

void doA()
{
  static bool a = digitalRead(ENCA);
  static bool b = digitalRead(ENCB);
  if (a == 0) //falling edge
  {
    if (b == 0) {
      count--;  //ccw
    }
    else if (b == 1) {
      count++;  //cw
    }
  }
  if (a == 1) //falling edge
  {
    if (b == 0) {
      count++;  //ccw
    }
    else if (b == 1) {
      count--;  //cw
    }
  }
}
void doB()
{
  static bool a = digitalRead(ENCA);
  static bool b = digitalRead(ENCB);
  if (b == 0) //falling edge
  {
    if (a == 0) {
      count--;  //cw
    }
    else if (a == 1) {
      count++;  //ccw
    }
  }
  if (b == 1) //falling edge
  {
    if (a == 0) {
      count++;  //ccw
    }
    else if (a == 1) {
      count--;  //cw
    }
  }
}
