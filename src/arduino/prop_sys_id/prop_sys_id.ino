#define DIRA 12
#define DIRB 13
#define PWMA 3
#define PWMB 11
#define ENCA 18
#define ENCB 19
#define PROP_ENC 20
#define ratio 51.0

unsigned long cur, prev, t0, t1;
unsigned long dt = 50000;
int power = 10;

// State machine vars
int state = 0;

//Ang vel vars
volatile int count, countprev = 0;

void setup() {
  Serial.begin(115200);
  pinMode(DIRA, OUTPUT);
  pinMode(DIRB, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(ENCA, INPUT_PULLUP);
  pinMode(ENCB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PROP_ENC), doA, CHANGE);
//  attachInterrupt(digitalPinToInterrupt(ENCB), doB, CHANGE);
  digitalWrite(DIRB, HIGH);
}

void loop() {
  cur = micros();
  switch (state)
  {
    case 0: //Set motor power
      analogWrite(PWMB, power);
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
        count = 0;
        state = 3;
        t0 = micros();
        t1 = micros();
        Serial.print("ANG VEL: ");
      }
      break;
    case 3: //Estimate Angvel, and print data for 10 sec, then increment power then go to state 0
      if ((cur - t0) >= 10000000) {
        state = 0;
        power += 10;
        if (power > 255) {
          power = 255;
        } Serial.println();
      }
      else if ((cur - t1) >= 50000) {
        //estimate angvel and print
        static double dt;
        dt = (cur - t0) / 1000000.0;
        static double angvel;
        angvel = 3.14159 * count / dt;
        Serial.print(" | "); Serial.print(calc_omega(count-countprev , 50000));
        countprev = count;
      }
      break;

  }

}

double calc_omega(double dcount, double dt)
{
  return dcount/(dt*ratio);
}

void doA()
{
  count++;
}

/* 9V
    PWM - grams
    10
    20
    30 0.80
    40 1.78
    50 2.75
    60 3.74
   70 4.66
   80 5.58
   90 - 6.50
   100 7.41
   110 8.23
   120 9.25
   130 10.00
   140 10.80
   150 - 11.62
   160 - 12.40
   170 - 13.25
   180 - 13.95
   190 - 14.48
   200 -
   210 - 1.70
   220 - 1.80
   230 - 1.95
   240 - 2.08
   250 - 2.14
   255 - 2.14


*/
