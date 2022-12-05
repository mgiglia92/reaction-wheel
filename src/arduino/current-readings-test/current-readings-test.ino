#define DIRA 12
#define DIRB 13
#define PWMA 3
#define PWMB 11
#define ENCA 18
#define ENCB 19
#define ratio 51.0
#define CURPIN A0
#define ARRLEN 100

unsigned long cur, prev, t0, t1,lastdt=0;
unsigned long dt = 50000;
uint16_t power = 70;

// State machine vars
int state = 0;

//Ang vel vars
volatile int count = 0;
int countprev = 0;
double wavg;


//Current readings
double current;
int raw_analog;
int raw[ARRLEN];
double cur_avg;
int i=0;

void setup() {
  Serial.begin(115200);
  pinMode(DIRA, OUTPUT);
  pinMode(DIRB, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(ENCA, INPUT_PULLUP);
  pinMode(ENCB, INPUT_PULLUP);
//  pinMode(CURPIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCA), doA, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCB), doB, CHANGE);
  digitalWrite(DIRA, HIGH);
  analogWrite(PWMA, 0);

  while (!Serial.available()) {}
  analogWrite(PWMA, power);
  prev=cur;
}

void loop() {
  cur = micros();
  if ((cur - prev) >= 200)
  {
    raw_analog = analogRead(CURPIN);
    raw[i] = raw_analog;
    i++; if(i>=ARRLEN){i=0;}
    lastdt = cur-prev;
    prev = cur;
  }
  if((cur-t1) >= 500000){
    cur_avg = get_avg(raw);
    Serial.print(cur_avg); Serial.print(','); Serial.print(lastdt); Serial.print(','); Serial.print(power);Serial.println();
    t1=cur;
  }
  if ((cur - t0) >= 10000000) {
    power += 10;
    analogWrite(PWMA, power);
    t0 = cur;
  }
}

double get_avg(int *raw)
{
  double avg=0;
  for(int j=0; j<ARRLEN; j++)
  {
    avg += raw[j];
  }
  return avg/ARRLEN;
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
